from matminer.featurizers.base import MultipleFeaturizer
from matminer.featurizers.composition import ElementProperty
from matminer.featurizers.conversions import StrToComposition
import pandas as pd

def get_magpie(df: pd.DataFrame, col: str):
    # get pymatgen composition objects from composition dictionaries
    df = StrToComposition(target_col_id="pmg_composition").featurize_dataframe(df, col)
    # convert composition into magpie features
    featurizer = MultipleFeaturizer([ElementProperty.from_preset("magpie")])
    df = featurizer.featurize_dataframe(df, col_id="pmg_composition")
    # remove the pmg_composition (extraneous) column
    df = df[[c for c in df.columns if c not in ["pmg_composition"]]]
    return df
