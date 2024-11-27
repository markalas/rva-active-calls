import utility
from webscraper import WebScraper
from utility import Utility
import time

url = "https://activecalls.henrico.gov"
webscraper_obj = WebScraper(url)
utility_obj = Utility

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