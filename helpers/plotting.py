from matplotlib import pyplot as plt
import matplotlib.animation as animation
import seaborn as sns

myrcparams = {
    'axes.labelsize': 24,
    'axes.titlesize': 24,
    'axes.xmargin': 0,
    'axes.ymargin': 0,
    'legend.fontsize': 24,
    'xtick.labelsize': 20,
    'ytick.labelsize': 20
}

def corrplot(df, figsize=(10,7)):
    """
    Plots a heatmap of the correlation matrix.

    Parameters
    ----------
    df : pandas dataframe 
            The feature correlation matrix
    figsize : tuple
            Size of the figure

    Returns
    -------
    None
    """
    fig,ax = plt.subplots(figsize = figsize)
    sns.set(font_scale = 1.5)
    sns.heatmap(df, annot = False, vmin = -1, vmax = 1, cmap = 'coolwarm')

def boxplot(df, features, nrows = 2, figsize = (15,10)):
    """
    Creates a boxplot for specified features.

    Parameters
    ----------
    df : pandas dataframe 
            Input data
    features : list-like
            List of features to plot
    nrows : int
            Number of rows in subplot
    figsize : tuple
            Size of figure

    Returns
    -------
    None
    """
    ncols = len(features) // nrows
    ind = np.unravel_index(range(len(features)), (nrows, ncols))
    fig, axes = plt.subplots(nrows = nrows, ncols = ncols, 
                                           figsize = figsize
                                           )
    boxprops = dict(linestyle='-', linewidth=1.5, facecolor='lavender', edgecolor='indigo')
    flierprops = dict(marker='o', markerfacecolor='lavender', markeredgecolor='indigo', markersize=8)
    whiskerprops = dict(linewidth=1.5, color='indigo')
    capprops = dict(linewidth=1.5, color='indigo')
    medianprops = dict(linewidth=1.5, linestyle='-', color='indigo')
    meanprops = dict(markerfacecolor='indigo', markeredgecolor='indigo', marker='^', markersize=8)
    if len(features) == 1:
        sns.boxplot(df[features[0]], ax = axes, showmeans = True, boxprops=boxprops, whiskerprops=whiskerprops,
                capprops=capprops, flierprops=flierprops, medianprops=medianprops, meanprops=meanprops) #boxplot 
                #will be created and a symbol will indicate the mean value of the column   

    else:
        for i,feature in enumerate(features):
            row = ind[0][i]
            col = ind[1][i]
            sns.boxplot(df[feature], ax = axes[row,col], showmeans = True, boxprops=boxprops, whiskerprops=whiskerprops,
                capprops=capprops, flierprops=flierprops, medianprops=medianprops, meanprops=meanprops) 
                #boxplot will be created and a symbol will indicate the mean value of the column   
    sns.set_color_codes()
    
def distplot(df, features, nrows = 2, figsize = (15,10), bins = None):
    """
    Creates a plot of the distributions for the specified features.

    Parameters
    ----------
    df : pandas dataframe 
            Input data
    features : list-like
            List of features to plot
    nrows : int
            Number of rows in subplot
    figsize : tuple
            Size of figure
    bins : None, 'auto', or int
            Number of bins 

    Returns
    -------
    None
    """
    ncols = len(features) // nrows
    ind = np.unravel_index(range(len(features)), (nrows, ncols))
    fig, axes = plt.subplots(nrows = nrows, ncols = ncols, 
                                           figsize = figsize
                                           )
    if len(features) == 1:
        sns.set_color_codes()
        if bins:
            sns.distplot(df[features[0]], kde = F, ax = axes, bins = bins, color="dodgerblue") 
        else:
            sns.distplot(df[features[0]], kde = False, ax = axes, color="dodgerblue") # For histogram
    
        axes.axvline(np.mean(df[features[0]]), color = 'blue', linestyle = '--', linewidth=1.7) # Add mean 
    
        axes.axvline(np.median(df[features[0]]), color = 'black', linestyle = '-', linewidth=1.6) # Add median
    else:
        for i,feature in enumerate(features):
            row = ind[0][i]
            col = ind[1][i]
            sns.set_color_codes()
            if bins:
                sns.distplot(df[feature], kde = F, ax = axes[row,col], bins = bins, color="dodgerblue")
            else: 
                sns.distplot(df[feature], kde = False, ax = axes[row,col], color="dodgerblue") # For histogram
    
            axes[row,col].axvline(np.mean(df[feature]), color = 'blue', linestyle = '--', linewidth=1.7) # Add mean 
    
            axes[row,col].axvline(np.median(df[feature]), color = 'black', linestyle = '-', linewidth=1.6) # Add median 

def predvtrue(y_true,y_pred):
    """
    Parity plot of predicted gaps vs. true gaps.

    Parameters
    ----------
    y_true : numpy array
            True gaps
    y_pred : numpy array
            Predicted gaps

    Returns
    -------
    None
    """ 
    
    plt.plot(y_true, y_true, color='black',linewidth=1.5)

    # Calculate the point density  
    xy = np.vstack([y_true,y_pred])
    z = stats.gaussian_kde(xy)(xy)

    # Sort the points by density, so that the most dense points are plotted last
    idx = z.argsort()
    y_true, y_pred, z = y_true[idx], y_pred[idx], z[idx]

    # scatter plot
    plt.scatter(y_true,y_pred,c=z,s=80,cmap="viridis")
    plt.xlabel(r'y$_\mathrm{test}$')
    plt.ylabel(r'y$_\mathrm{pred}$')
