from pandas import DataFrame
import smtplib
import pandas as pd
import datetime as dt
import os


class Utility:

    def __init__(self):
        self.datetime = dt.datetime.today().strftime('%Y-%m-%d_%I%M%S')
        self.filename = f'active_calls_{self.datetime}.xlsx'

    def df_split_column(df: DataFrame, col_name, new_col_name1, new_col_name2, delimiter) -> DataFrame:
        df[[new_col_name1, new_col_name2]] = df[col_name].str.split(delimiter, expand=True)
        return df
    
    def output_excel(self, df: DataFrame):
        if not os.path.exists(self.filename):
            df.to_excel(self.filename, engine='xlsxwriter', index=False)
        else:
            with pd.ExcelWriter(self.filename, 'a') as writer:
                df.to_excel(writer)

    def excel_to_df(self, filename: str) -> DataFrame:
        df = pd.read_excel(filename)
        return df

