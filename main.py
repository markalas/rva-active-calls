from webscraper import WebScraper
from utility import Utility
import time
import pandas as pd
import itertools

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
# lst2 = [{8988, 'ENROUTE 14:42'}, {8971, 'ARRIVED 14:17'}, {8946, 'ARV TRNSPT 14:53'}]

# for i, j in zip(lst1, lst2):
#     if i == j:
#         print('match')
#     else:
#         print('no match', i, j)


# exit()



df = pd.DataFrame()
while True:
    if len(df) <= 0:
        df_init = webscraper_obj.dataframe_output()
        df = df_init
        print(df)
    else:
        # if df is not 0 then start comparison, hit the website again after 5 sec, store in dataframe then see if df = df_compare
        time.sleep(5)
        df_compare = webscraper_obj.dataframe_output()
        if len(df) == len(df_compare):
            df_lst1 = []
            df_lst2 = []
            for i in range(len(df)):
                dict1 = {df.loc[i, "ID"], df.loc[i, "Call Status"]}
                dict2 = {df_compare.loc[i, "ID"], df_compare.loc[i, "Call Status"]}
                df_lst1.append(dict1)
                df_lst2.append(dict2)
            
            for i, j in zip(df_lst1, df_lst2):
                if i == j:
                    print("No Status Update")
                else:
                    print('Status Update')


