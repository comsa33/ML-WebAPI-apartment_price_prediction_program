import requests
import xmltodict, json


Encoding = "F9JRa0SmO1YC0LOweI2DUZO%2BLuqgg3ckPbplWoFkaQkVHLC87cgFrWPLq8476LXHiId5e0jGCQvwsOCffNrN1Q%3D%3D"
Decoding = "F9JRa0SmO1YC0LOweI2DUZO+Luqgg3ckPbplWoFkaQkVHLC87cgFrWPLq8476LXHiId5e0jGCQvwsOCffNrN1Q=="

url = 'http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev'
params ={'serviceKey' : Decoding, 'pageNo' : '1', 'numOfRows' : '10', 'LAWD_CD' : '11110', 'DEAL_YMD' : '201512' }

response = requests.get(url, params=params)
print(response.content)