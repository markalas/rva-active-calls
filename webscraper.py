import requests
import pandas as pd
from pandas import DataFrame
from io import StringIO
from bs4 import BeautifulSoup

class WebScraper:
    
    def __init__(self, url):
        self.url = url

    def request_url(self):
        try:
            response = requests.get(self.url)
            content = response.content
            status = response.status_code
            return content, status
        except Exception as ex:
            print(f'Exception in WebScraper.request_url ::: Unable to get {self.url} status is {status} ::: Exception ::: {ex}')
        return None

    def parse_html(self):
        parser = 'html.parser'
        html_target_tag = 'table'

        try:
            content, status = self.request_url()
            if status == 200:
                html_content = BeautifulSoup(content, parser)
                html_target = html_content.find_all(html_target_tag)
                return html_target
        except Exception as ex:
            print(f'Exception in WebScraper.parse_html ::: Unable to find {html_target} ::: Exception ::: {ex}')
        return None
        
    def html_to_io(self):
        html_str = str(self.parse_html())
        html_io = StringIO(html_str)
        return html_io
    
    def dataframe_output(self) -> DataFrame:
        html_str = self.html_to_io()

        try:
            self.df = pd.read_html(html_str)
            self.df = self.df[0]
            self.df['Previous Call Status'] = ""
            self.df['Call Status Indicator'] = ""
            return self.df
        except ValueError as ex:
            print(f'Error in Webscraper.dataframe_output ::: ValueError ::: {ex}')
        return None
            



