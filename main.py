import utility
from webscraper import WebScraper
from utility import Utility
import time
import pandas as pd

url = "https://activecalls.henrico.gov"
webscraper_obj = WebScraper(url)
utility_obj = Utility

"""
create dataframe obj
    if dataframe obj is empty, add data
    once dataframe obj has data add/update records based on ID and Status
    add an indicator to the dataframe that shows New Call or Update Call  
        on Update Call replace the Status for that ID
    print dataframe obj only if there is an update or added record
"""


df = pd.DataFrame()
print(df)
while True:
    if len(df) <= 0:
        df_init = webscraper_obj.dataframe_output()
        df = df_init
    else:
        # if df is not 0 then start comparison, hit the website again after 5 sec, store in dataframe then see if df = df_compare
        time.sleep(5)
        df_compare = webscraper_obj.dataframe_output()




while True:
    time.sleep(5)
    print(f'\nData from {url}\n')
    df = webscraper_obj.dataframe_output()
    utility_obj.df_split_column(df=df, col_name='Call Status', new_col_name1='Status', new_col_name2='Status Time', delimiter='\s(?=\d)')
    df.drop(['Call Status'],axis=1, inplace=True)
    df.sort_values(by=['ID'], ascending=True)

    active_calls = len(df)
    
    
    if active_calls < 1:
        print(f'No Active calls. Listening...')
    else:
        print(f'There are {active_calls} active calls\n')
        print(df)


