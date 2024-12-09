from pandas import DataFrame
from log_handler import LogHandler
import smtplib
import pandas as pd
import datetime as dt
import os

class Utility:

    def __init__(self):

        # set file attributes
        self.datetime = dt.datetime.today().strftime('%Y-%m-%d_%I%M%S')
        self.filename_xlsx = f'active_calls_{self.datetime}.xlsx'

        # instantiate logger class
        self.log_handler_obj = LogHandler(self.datetime)

    @property
    def log_handler(self):
        return self.log_handler_obj

    def df_split_column(df: DataFrame, col_name, new_col_name1, new_col_name2, delimiter) -> DataFrame:
        df[[new_col_name1, new_col_name2]] = df[col_name].str.split(delimiter, expand=True)
        return df
    
    def output_excel(self, df: DataFrame):
        if not os.path.exists(self.filename_xlsx):
            df.to_excel(self.filename_xlsx, engine='xlsxwriter', index=False)
        else:
            with pd.ExcelWriter(self.filename_xlsx, 'a') as writer:
                df.to_excel(writer)

    def excel_to_df(self, filename: str) -> DataFrame:
        df = pd.read_excel(filename)
        return df
