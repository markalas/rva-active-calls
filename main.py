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