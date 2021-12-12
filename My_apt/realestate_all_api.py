import requests
import xmltodict, json
from pprint import pprint

Encoding = "F9JRa0SmO1YC0LOweI2DUZO%2BLuqgg3ckPbplWoFkaQkVHLC87cgFrWPLq8476LXHiId5e0jGCQvwsOCffNrN1Q%3D%3D"
Decoding = "F9JRa0SmO1YC0LOweI2DUZO+Luqgg3ckPbplWoFkaQkVHLC87cgFrWPLq8476LXHiId5e0jGCQvwsOCffNrN1Q=="

url = 'http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev'
params ={'ServiceKey' : Encoding, 'pageNo' : '1', 'numOfRows' : '1', 'LAWD_CD' : '11110', 'DEAL_YMD' : '202011' }

response = requests.get(url, params=params)
obj = xmltodict.parse(response.content)
result = json.dumps(obj, ensure_ascii=False)
pprint(result)

