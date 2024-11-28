from io import StringIO
import requests
import pandas as pd
from bs4 import BeautifulSoup

class WebScraper:
    
    def __init__(self, url):
        self.url = url

    def request_url(self):
        response = requests.get(self.url)
        content = response.content
        status = response.status_code
        return content, status

    def parse_html(self):
        parser = 'html.parser'
        html_target_tag = 'table'
        content, status = self.request_url()

        try:
            if status == 200:
                html_content = BeautifulSoup(content, parser)
                html_target = html_content.find_all(html_target_tag)
                return html_target
        except Exception as ex:
            print(f'Exception in WebScraper.parse_html : Exception : {ex}')
        return None
        
    def html_to_io(self):
        html_str = str(self.parse_html())
        html_io = StringIO(html_str)
        return html_io
    
    def dataframe_output(self):
        html_str = self.html_to_io()

        try:
            self.df = pd.read_html(html_str)
            return self.df[0]
        except ValueError as ex:
            print(f'Error in Webscraper.dataframe_output : ValueError : {ex}')
        return None
            



