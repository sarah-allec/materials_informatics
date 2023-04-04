import pandas as pd
import torch
from sklearn.model_selection import train_test_split as split
from aviary import ROOT
from aviary.roost.data import CompositionData, collate_batch
from aviary.roost.model import Roost
from aviary.utils import results_multitask, train_ensemble

def train(X, Y, val_size=0.0, val_path=None,
          resume=None, fine_tune=None, transfer=None):
          
    df = pd.concat( [X,Y], axis=1)
    df.insert(0,'material_id',[0]*len(df))

    if isinstance(Y, pd.DataFrame):
        targets = Y.columns.tolist
        tasks = ['regression']*len(targets)
        losses = ['L1']*len(targets)
    if isinstance(Y, pd.Series):
        targets = [Y.name]
        tasks = ['regression']
        losses = ['L1']

    task_dict = dict(zip(targets, tasks))
    loss_dict = dict(zip(targets, losses))
    device = "cuda" if torch.cuda.is_available() else "cpu"

    elem_embedding = "matscholar200"
    dataset = CompositionData(df=df, elem_embedding=elem_embedding, task_dict=task_dict)

    n_targets = dataset.n_targets
    elem_emb_len = dataset.elem_emb_len

    train_idx = list(range(len(dataset)))
    evaluate = False

    if val_path:

        if not os.path.isfile(val_path):
            raise AssertionError(f"{val_path} does not exist!")
        # NOTE make sure to use dense datasets,
        # NOTE do not use default_na as "NaN" is a valid material
        df = pd.read_csv(val_path, keep_default_na=False, na_values=[])

        print(f"using independent validation set: {val_path}")
        val_set = CompositionData(
            df=df, elem_embedding=elem_embedding, task_dict=task_dict
        )
        val_set = torch.utils.data.Subset(val_set, range(len(val_set)))
    else:
        if val_size == 0.0 and evaluate:
            print("No validation set used, using test set for evaluation purposes")
            # NOTE that when using this option care must be taken not to
            # peak at the test-set. The only valid model to use is the one
            # obtained after the final epoch where the epoch count is
            # decided in advance of the experiment.
            val_set = test_set
        elif val_size == 0.0:
            val_set = None
        else:
            print(f"using {val_size} of training set as validation set")
            train_idx, val_idx = split(
                train_idx,
                random_state=data_seed,
                test_size=val_size / (1 - test_size),
            )
            val_set = torch.utils.data.Subset(dataset, val_idx)
    sample = 1
    train_set = torch.utils.data.Subset(dataset, train_idx[0::sample])

    data_params = {
        "batch_size": 128,
        "num_workers": 0,
        "pin_memory": False,
        "shuffle": True,
        "collate_fn": collate_batch,
    }

    setup_params = {
        "optim": "AdamW",
        "learning_rate": 3e-4,
        "weight_decay": 1e-6,
        "momentum": 0.9,
        "device": device,
    }

    restart_params = {
        "resume": resume,
        "fine_tune": fine_tune,
        "transfer": transfer,
    }

    model_params = {
        "task_dict": task_dict,
        "robust": True,
        "n_targets": n_targets,
        "elem_emb_len": elem_emb_len,
        "elem_fea_len": 64,
        "n_graph": 3,
        "elem_heads": 3,
        "elem_gate": [256],
        "elem_msg": [256],
        "cry_heads": 3,
        "cry_gate": [256],
        "cry_msg": [256],
        "trunk_hidden": [1024, 512],
        "out_hidden": [256, 128, 64]
    }

    # TODO dump all args/kwargs to a file for reproducibility.

    if train:
        train_ensemble(
            model_class=Roost,
            model_name="roost",
            run_id=0,
            ensemble_folds=1,
            epochs=250,
            patience=None,
            train_set=train_set,
            val_set=val_set,
            log=True,
            data_params=data_params,
            setup_params=setup_params,
            restart_params=restart_params,
            model_params=model_params,
            loss_dict=loss_dict,
        )

def predict(X,target,y_test=None):
    if y_test is None:
        df = pd.DataFrame( np.column_stack( ( [0]*len(X), X, [0]*len(X) ) ), columns=['material_id', 'composition', target] )
    else:
        df = pd.DataFrame( np.column_stack( ( [0]*len(X), X, y_test ) ), columns=['material_id', 'composition', target] )

    targets = [target]
    tasks=["regression"] 
    task_dict = dict(zip(targets, tasks))
    model_name="roost"
    ensemble=1
    device=None
    robust = True
    batch_size = 128
    workers = 0
    data_params = {
        "batch_size": batch_size,
        "num_workers": workers,
        "pin_memory": False,
        "shuffle": True,
        "collate_fn": collate_batch,
    }
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
    
    X = CompositionData(df[ [ 'material_id', 'composition', targets[0]] ], elem_embedding = "matscholar200", task_dict = task_dict)
    test_set = torch.utils.data.Subset(X, range(len(X))) 
    run_id=0
    results_dict = results_multitask( 
         model_class=Roost, 
         model_name=model_name,
         run_id=run_id, 
         ensemble_folds=ensemble, 
         test_set=test_set, 
         data_params=data_params, 
         robust=robust, 
         task_dict=task_dict, 
         device=device, 
         eval_type="checkpoint", 
         save_results=False,
    )
    target_name = targets[0] 
    preds = results_dict[target_name]["preds"][0] 
    true = results_dict[target_name]["targets"]
    return preds, true   
     
