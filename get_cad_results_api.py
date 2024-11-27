import json
import requests
import datetime as dt
import xmltodict

class GetCADResultsAPI:

    def get_posts():
        
        posts = []

        url = "https://ppd.henrico.gov/webservices/cadservice.asmx/GetCadResults"
        date_today = dt.datetime.now().date() - dt.timedelta(days=1)
        str_start_date = str(date_today)

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "ppd.henrico.gov"
        }

        params = {
            "strServiceArea":"",
            "strSRA":"",
            "strMagisDist":"",
            "strStartDate": str_start_date,
            "strEndDate":"",
            "strNeigoboorhoodWatch":"",
            "strStreetName":"",
            "strDirection":"",
            "strStreetType":"",
            "strFinalCallType":"",
            "strDisposition":""
        }
        print(params["strStartDate"])
        response = requests.get(url=url, headers=headers, params=params, stream=True)
        
        xmlparse = xmltodict.parse(response.text)
        posts = json.dumps(xmlparse)

        return posts
    


cad_api = GetCADResultsAPI

print(cad_api.get_posts())