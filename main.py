from numpy import isin
from webscraper import WebScraper
from utility import Utility
import numpy as np
import time
import pandas as pd
import itertools
import datetime as dt

url = "https://activecalls.henrico.gov"
webscraper_obj = WebScraper(url)
utility_obj = Utility()

"""
create dataframe obj
    if dataframe obj is empty, add data
    once dataframe obj has data add/update records based on ID and Status
    add an indicator to the dataframe that shows New Call or Update Call
        on Update Call replace cthe Status for that ID
    print dataframe obj only if there is an update or added record
"""
# lst1 = [{8988, 'ENROUTE 14:42'}, {8971, 'ARRIVED 14:17'}, {8946, 'ARV TRNSPT 14:53'}]
# lst2 = [{8988, 'ENROUTE 14:42'}, {8971, 'ARRIVED 14:17'}, {8946, 'ARV TRNSPT 14:54'}]

# for i, j in zip(lst1, lst2):
#     if i == j:
#         print('match')
#     else:
#         print('difference', i, j)


# exit()

# define method for comparison which takes dataframes as arguments

df = pd.DataFrame()
while True:
    if len(df) == 0:
        df_init = webscraper_obj.dataframe_output()
        # df_init = utility_obj.excel_to_df('active_calls_2024-12-03_012529.xlsx')
        df = df_init
        print(f'\n{df}\n')
    else:
        # if df is not 0 then start comparison, hit the website again after 5 sec, store in dataframe then see if df = df_compare
        time.sleep(5)
        df_compare = webscraper_obj.dataframe_output()
        datetime = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # df_compare = utility_obj.excel_to_df('active_calls_2024-12-03_012535.xlsx')
        df_start_lst = [{'ID': row['ID'], 'Call Status': row['Call Status']} for _, row in df.iterrows()]
        df_compare_lst = [{'ID': row['ID'], 'Call Status': row['Call Status']} for _, row in df_compare.iterrows()]

        # print(df_init)
        # print(df_start_lst, df_compare_lst)

        if len(df_start_lst) > len(df_compare_lst):
            print('rows removed')
            lst_diff = [val for val in df_start_lst if val not in df_compare_lst]
            lst_init = [val for val in df_start_lst]

            for item_diff in lst_diff:
                diff_id = int(item_diff['ID'])
                diff_id_idx = df[df['ID'] == diff_id].index
                print(f'removing record: {diff_id}')
                df.drop(diff_id_idx, inplace=True)
                print(df)

        elif len(df_start_lst) < len(df_compare_lst):
            # first check if any of the previous records had an update
            # add new rows after
            print('rows added')
            lst_diff = [val for val in df_compare_lst if val not in df_start_lst]
            lst_init = [val for val in df_start_lst]

            for item_diff in lst_diff:
                diff_id = int(item_diff['ID'])
                new_status = item_diff['Call Status']
                is_empty_df = df.loc[df['ID'] == diff_id].empty

                if is_empty_df:
                    print(f'adding record: {diff_id}')
                    new_record_df = df_compare.loc[df_compare['ID']==diff_id]
                    df = pd.concat([df, new_record_df], ignore_index=True)
                    print(df)
                else:
                    previous_status = df.loc[df['ID'] == diff_id, 'Call Status'].values[0]
                    if previous_status != new_status:
                        print(f'updating record: {diff_id}')
                        df.loc[df['ID'] == diff_id, 'Previous Call Status'] = df.loc[df['ID'] == diff_id, 'Call Status']
                        df.loc[df['ID'] == diff_id, 'Call Status'] = new_status
                        df.loc[df['ID'] == diff_id, 'Call Status Indicator'] = datetime
                        print(df)
                    else:
                        pass
        else:
            # print('updating statuses')
            lst_diff = [val for val in df_compare_lst]
            lst_init = [val for val in df_start_lst]

            for item_diff in lst_diff:
                diff_id = int(item_diff['ID'])
                new_status = item_diff['Call Status']
                previous_status = df.loc[df['ID'] == diff_id, 'Call Status'].values[0]

                if previous_status != new_status:
                    print(f'updating record: {diff_id}')
                    df.loc[df['ID'] == diff_id, 'Previous Call Status'] = df.loc[df['ID'] == diff_id, 'Call Status']
                    df.loc[df['ID'] == diff_id, 'Call Status'] = new_status
                    df.loc[df['ID'] == diff_id, 'Call Status Indicator'] = datetime
                    print(df)
                else:
                    pass