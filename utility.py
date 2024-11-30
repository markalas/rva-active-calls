import smtplib
import pandas as pd
from pandas import DataFrame

class Utility:

    def df_split_column(df: DataFrame, col_name, new_col_name1, new_col_name2, delimiter) -> DataFrame:
        df[[new_col_name1, new_col_name2]] = df[col_name].str.split(delimiter, expand=True)
        return df
    
    def update_df(self):
        pass