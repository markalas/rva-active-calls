from webscraper import WebScraper
from utility import Utility
import time
import pandas as pd
import itertools
import datetime as dt

url = "https://activecalls.henrico.gov"
webscraper_obj = WebScraper(url)
utility_obj = Utility

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

df = pd.DataFrame()
while True:
    if len(df) == 0:
        df_init = webscraper_obj.dataframe_output()
        df = df_init
        print(df)
    else:
        # if df is not 0 then start comparison, hit the website again after 5 sec, store in dataframe then see if df = df_compare
        time.sleep(5)
        df_compare = webscraper_obj.dataframe_output()
        df_updated = pd.DataFrame()

        if len(df) == len(df_compare):
            df_lst1 = [] 
            df_lst2 = []
            # Store ID and status from both dataframes
            for i in df.index:
                dict1 = {"Idx": i, 
                        "Call Status": df.loc[i, "Call Status"]}
                dict2 = {"Idx": i,
                        "Call Status": df_compare.loc[i, "Call Status"]}
                
                df_lst1.append(dict1), df_lst2.append(dict2)
            
            # Find differences in the dataframe by comparing them in a list
            for i, j in zip(df_lst1, df_lst2):
                if i == j:
                    # do nothing
                    pass 
                else:
                    datetime = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    status_indicator = f'Updated Status @ {datetime}' # indicator for an updated call status
                    df_previous_status_val = i['Call Status']
                    df_compare_updated_status_val = j['Call Status'] # updated status from df2
                    update_idx = j['Idx'] # index location in dataframe 2

                    df.at[update_idx, 'Call Status'] = df_compare_updated_status_val # updating call status in df to updated value
                    df.at[update_idx, 'Call Status Indicator'] = status_indicator # updating status indicator in df
                    df_updated = df # store df to df_updated

                    df_updated_previous_status_val = df_updated['Previous Call Status'].iloc[update_idx]

                    if df_updated['Previous Call Status'].iloc[update_idx] == "":
                        df_updated.at[update_idx, 'Previous Call Status'] = df_previous_status_val
                    else:
                        df_updated.at[update_idx, 'Previous Call Status'] = df_updated_previous_status_val

                    print(df_updated)
        else:
            if len(df) > len(df_compare):
                print('updated df: rows removed')
                df = df_updated
            elif len(df) < len(df_compare):
                print('updated df: rows added')
                df = df_updated
            
        # else:
        #     if len(df) > len(df_compare):
        #         print("record removed")
        #     else:
        #         print("record added ")



            #     c   p
            # 1   1   
            # 2   2   1
            # 3   3   2
