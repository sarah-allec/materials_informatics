from sklearn.metrics import r2_score, mean_absolute_error
import numpy as np
import gpflow

# Method for updating training data based on acquisition functions
def update(X, y, y_pred, y_std, train_inds, acq = 'mei', n = 1):
    all_inds = set(range(len(X))) # indices for entire dataset
    search_inds = list(all_inds.difference(train_inds)) # test set indices
    acq = acq.lower()
    if acq == 'mei':
        return train_inds + [search_inds[s] for s in y_pred.argsort()[::-1][:n]]
    elif acq == 'mli':
        return train_inds + [search_inds[s] for s in (np.divide(y_pred-np.max(y),y_std)).argsort()[::-1][:n]]
    elif acq == 'mu':
        return train_inds + [search_inds[s] for s in y_std.argsort()[::-1][:n]]
    else:
        return train_inds + [s for s in np.random.choice(search_inds, n)] 
    
# Method for running the active learning loop    
def run(X, y, n_start = 20, n_steps = 10, n_inc = 1, acq='mu'):
    # Select initial training set
    np.random.seed(100)
    in_train = np.zeros(len(X), dtype=bool)
    in_train[np.random.choice(len(X), n_start, replace=False)] = True
    
    all_inds = set(range(len(y)))
    train = [np.where(in_train)[0].tolist()]
    train_inds = train[-1].copy()    # Initial Set
    search_inds = list(all_inds.difference(train_inds)) # All samples not in the current set
    
    # Active learning steps
    y_max = []
    train = [np.where(in_train)[0].tolist()]
    for i in range(n_steps):
        train_inds = train[-1].copy()    # Initial Set
        search_inds = list(all_inds.difference(train_inds)) # All samples not in the current set
        model = gpflow.models.GPR(
                                   (X[train_inds], y[train_inds]),
                                    kernel=gpflow.kernels.Matern12(),
                                  )
        opt = gpflow.optimizers.Scipy()
        opt.minimize(model.training_loss, model.trainable_variables)
        y_pred, y_unc = model.predict_y(X[search_inds]) # Predictions
    
        y_pred = y_pred.numpy().squeeze()
        y_unc = y_unc.numpy().squeeze()
        r2 = r2_score(y[search_inds], y_pred)
        if r2 > 0.2 and acq == 'mu':
            acq = 'mli'
        y_max.append( max( y[train_inds] )[0] )
        if max( y[train_inds] )[0] == max(y):
            return y_max, model, train_inds

        # Update training set
        train_inds = update(X, y[train_inds], y_pred, y_unc, train_inds, acq=acq, n=n_inc)
        train.append(train_inds) # Storage of the current set per step
        
    return y_max, model, train_inds
