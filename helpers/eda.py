from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from itertools import combinations

def corr_filter(df, threshold):
    # Drop one of each highly correlated pair
    df_corr = df.corr()
    c = df_corr.abs()
    
    s = c.unstack()
    so = s.sort_values(kind="quicksort")
    corr_var = so[ (so >= 0.8) & (so < 1.0) ].drop_duplicates()
    
    neg_corr = {}
    pos_corr = {}
    for pair in corr_var.index:
        this_corr = df_corr.loc[pair[0], pair[1]]
        if this_corr > 0:
            pos_corr[pair] = this_corr
        else:
            neg_corr[pair] = this_corr
    for key, value in pos_corr.items():
        print(key, ' : ', value)
        if key[0] in df.columns:
            df.drop(columns = key[0], inplace = True)
        else:
            if key[1] in df.columns:
                df.drop(columns = key[1], inplace = True)
    for key, value in neg_corr.items():
        print(key, ' : ', value)
        if key[0] in df.columns:
            df.drop(columns = key[0], inplace = True)
        else:
            if key[1] in df.columns:
                df.drop(columns = key[1], inplace = True)
    return df
