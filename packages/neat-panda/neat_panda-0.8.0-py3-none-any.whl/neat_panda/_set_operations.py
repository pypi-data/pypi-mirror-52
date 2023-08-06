# -*- coding: utf-8 -*-

from typing import Optional, List

import pandas as pd
import pandas_flavor as pf


@pf.register_dataframe_method
def difference(dataframe1: pd.DataFrame, dataframe2: pd.DataFrame):
    if not dataframe1.columns.to_list() == dataframe2.columns.to_list():
        raise ValueError("The columns in the two columns must be exactly the same.")
    # return dataframe1[~dataframe1.apply(tuple, 1).isin(dataframe2.apply(tuple, 1))]
    return pd.concat([dataframe1, dataframe2, dataframe2]).drop_duplicates(keep=False)
    # https://stackoverflow.com/questions/48647534/python-pandas-find-difference-between-two-data-frames


@pf.register_dataframe_method
def symmmetric_difference(
    dataframe1: pd.DataFrame,
    dataframe2: pd.DataFrame,
    dataframe_names: Optional[List[str]] = None,
) -> pd.DataFrame:
    if not dataframe1.columns.to_list() == dataframe2.columns.to_list():
        raise ValueError("The columns in the two columns must be exactly the same.")
    if dataframe_names and len(dataframe_names) != 2:
        raise ValueError("Only two dataframe names")

    df1 = difference(dataframe1=dataframe1, dataframe2=dataframe2)
    df2 = difference(dataframe1=dataframe2, dataframe2=dataframe1)
    if dataframe_names:
        df1["original_dataframe"] = dataframe_names[0]
        df2["original_dataframe"] = dataframe_names[1]
    return pd.concat([df1, df2]).reset_index(drop=True)


@pf.register_dataframe_method
def intersection(dataframe1: pd.DataFrame, dataframe2: pd.DataFrame) -> pd.DataFrame:
    if not dataframe1.columns.to_list() == dataframe2.columns.to_list():
        raise ValueError("The columns in the two columns must be exactly the same.")
    return dataframe1.merge(right=dataframe2, how="inner")
    # http://www.datasciencemadesimple.com/intersection-two-dataframe-pandas-python-2/


if __name__ == "__main__":
    pass
