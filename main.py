from ctypes import util
from numpy import isin
from webscraper import WebScraper
from utility import Utility
import numpy as np
import time
import pandas as pd
import itertools
import datetime as dt

"""
create dataframe obj
    if dataframe obj is empty, add data
    once dataframe obj has data add/update records based on ID and Status
    add an indicator to the dataframe that shows New Call or Update Call
        on Update Call replace cthe Status for th at ID
    print dataframe obj only if there is an update or added record
"""

url = "https://activecalls.henrico.gov"
utility_obj = Utility()
logger = utility_obj.log_handler
webscraper_obj = WebScraper(url, utility_obj)

# define method for comparison which takes dataframes as arguments
logger.info_message('Start')
try:

    df = pd.DataFrame()
    while True:
        
        if len(df) == 0:
            df_init = webscraper_obj.dataframe_output()
            # df_init = utility_obj.excel_to_df('active_calls_2024-12-03_012529.xlsx')
            df = df_init
            print(f'\n{df}\n')
        else:
            # if df is not 0 then start comparison, hit the website again after 5 sec, store in dataframe then see if df = df_compare
            time.sleep(30)
            df_compare = webscraper_obj.dataframe_output()
            datetime = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # df_compare = utility_obj.excel_to_df('active_calls_2024-12-03_012535.xlsx')
            
            df_start_lst = [{'ID': row['ID'],
                            'Location': row['Block/Intersection'],
                            'Time Received': row['Received At'] ,
                            'District': row['Mag. Dist.'] ,
                            'Incident': row['Incident'],
                            'Call Status': row['Call Status']} 
                            for _, row in df.iterrows()
                        ]
            df_compare_lst = [{'ID': row['ID'],
                            'Location': row['Block/Intersection'],
                            'Time Received': row['Received At'] ,
                            'District': row['Mag. Dist.'] ,
                            'Incident': row['Incident'],
                            'Call Status': row['Call Status']} 
                            for _, row in df_compare.iterrows()
                            ]

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
                        try:
                            previous_status = df.loc[df['ID'] == diff_id, 'Call Status'].values[0]
                            if previous_status != new_status:
                                print(f'updating record: {diff_id}')
                                df.loc[df['ID'] == diff_id, 'Previous Call Status'] = df.loc[df['ID'] == diff_id, 'Call Status']
                                df.loc[df['ID'] == diff_id, 'Call Status'] = new_status
                                df.loc[df['ID'] == diff_id, 'Call Status Indicator'] = datetime
                                print(df)
                            else:
                                pass
                        except IndexError as ex:
                            err_message = f'Add rows for loop ::: IndexError ::: {diff_id} not in df'
                            logger.error_message(err_message)
                            print(err_message)
            else:
                # print('updating statuses')
                # add additional checks because if dfs are of both same length a record could have been deleted
                # and added at the same time

                # first check for deleted records
                lst_diff = [val for val in df_compare_lst]
                lst_init = [val for val in df_start_lst]

                for item_diff in lst_diff:
                    diff_id = int(item_diff['ID'])
                    new_status = item_diff['Call Status']

                    try:
                        previous_status = df.loc[df['ID'] == diff_id, 'Call Status'].values[0]
                        if previous_status != new_status:
                            print(f'updating record: {diff_id}')
                            df.loc[df['ID'] == diff_id, 'Previous Call Status'] = df.loc[df['ID'] == diff_id, 'Call Status']
                            df.loc[df['ID'] == diff_id, 'Call Status'] = new_status
                            df.loc[df['ID'] == diff_id, 'Call Status Indicator'] = datetime
                            print(df)
                        else:
                            pass
                    except IndexError as ex:
                        err_message = f'Update status only loop ::: IndexError ::: {diff_id} not in df'
                        logger.error_message(err_message)
                        print(err_message)
except KeyboardInterrupt:
    logger.info_message('Keyboard interrupt. Exiting..')
    logger.info_message('Finish')