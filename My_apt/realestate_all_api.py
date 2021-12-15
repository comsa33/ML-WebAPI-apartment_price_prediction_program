import requests
import xmltodict, json
from pymongo import MongoClient
from pprint import pprint
import pandas as pd
import time
import sqlite_all_apt

def get_lawd_cd():
    file = pd.read_csv('./My_apt/lawd_cd.txt', encoding='cp949')
    file = file.applymap(lambda x: x[:5])
    lawd_cd = file['법정동코드\t법정동명\t폐지여부'].unique()
    return lawd_cd

def get_ymd(start=2017, end = 2021):
    years = range(start, end+1)
    months = range(1, 13)
    ymd = []
    for year in years:
        for month in months:
            ymd.append(str(year)+str(month).zfill(2))
    return ymd

def get_result(pageNo,LAWD_CD, DEAL_YMD):
    Encoding = "F9JRa0SmO1YC0LOweI2DUZO%2BLuqgg3ckPbplWoFkaQkVHLC87cgFrWPLq8476LXHiId5e0jGCQvwsOCffNrN1Q%3D%3D"
    Decoding = "F9JRa0SmO1YC0LOweI2DUZO+Luqgg3ckPbplWoFkaQkVHLC87cgFrWPLq8476LXHiId5e0jGCQvwsOCffNrN1Q=="

    url = 'http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev'
    params ={
        'serviceKey' : Decoding, 
        'pageNo' : f'{pageNo}', 
        'numOfRows' : '100', 
        'LAWD_CD' : f'{LAWD_CD}', 
        'DEAL_YMD' : f'{DEAL_YMD}'
        }
    
    response = requests.get(url, params=params)
    print(response.status_code)
    print(response.content)

    time.sleep(0.1)
    obj = xmltodict.parse(response.content)
    contents = obj['response']['body']['items']
    
    try:
        result_ls = obj['response']['body']['items']['item']
    except:
        result_ls = None
        print(f'No Data {LAWD_CD}')
        pass

    return result_ls, contents


def connect_mongo():
    username = "ruo"
    password = "160813"
    URI = f"mongodb+srv://{username}:{password}@cluster0.yisdq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    client = MongoClient(URI)
    return client

def drop_collection(client):
    my_db = client['Real_Estate']
    coll_name = 'Apt_Sales'
    my_coll = my_db[coll_name]
    my_coll.drop()

def insert_data(client, json_files):
    my_db = client['Real_Estate']
    coll_name = 'Apt_Sales'
    my_coll = my_db[coll_name]
    my_coll.insert_many(json_files)

def load_data_to_mongo():
    client = connect_mongo()
    drop_collection(client)
    lawd_cd_ls = list(get_lawd_cd())[264:]
    valid_code = ['11110', '11140', '11170', '11200', '11215', '11230', '11260', '11290', '11305', '11320', '11350', '11380', '11410', '11440', '11470', '11500', '11530', '11545', '11560', '11590', '11620', '11650', '11680', '11710', '11740', '26110', '26140', '26170', '26200', '26230', '26260', '26290', '26320', '26350', '26380', '26410', '26440', '26470', '26500', '26530', '26710', '27110', '27140', '27170', '27200', '27230', '27260', '27290', '27710', '28110', '28140', '28177', '28185', '28200', '28237', '28245', '28260', '28710', '29110', '29140', '29155', '29170', '29200', '30110', '30140', '30170', '30200', '30230', '31110', '31140', '31170', '31200', '31710', '36110', '41111', '41113', '41115', '41117', '41131', '41133', '41135', '41150', '41171', '41173', '41190', '41210', '41220', '41250', '41271', '41273', '41281', '41285', '41287', '41290', '41310', '41360', '41370', '41390', '41410', '41430', '41450', '41461', '41463', '41465', '41480', '41500', '41550', '41570', '41590', '41610', '41630', '41650', '41670', '41800', '41820', '41830', '42110', '42130', '42150', '42170', '42190', '42210', '42230', '42720', '42730', '42750', '42760', '42770', '42780', '42790', '42800', '42810', '42820', '42830', '43111', '43112', '43113', '43114', '43130', '43150', '43720', '43730', '43740', '43745', '43750', '43770', '43800', '44131', '44133', '44150', '44180', '44200']
    code = valid_code + lawd_cd_ls
    ymd = get_ymd(2017, 2021)
    for deal_ymd in ymd:
        print(deal_ymd)
        for lawd_cd in code:
            print(lawd_cd)
            f_, c_, = get_result(1, lawd_cd, deal_ymd)
            if f_ == None:
                continue
            for page_num in range(1, 100):
                print(page_num)
                try:
                    json_files, contents = get_result(page_num, lawd_cd, deal_ymd)
                    if contents == None:
                        break
                    insert_data(client, json_files)
                except:
                    print('Error Occured While parsing from API!')
                    pass

if __name__ == '__main__':
    load_data_to_mongo()
    # json_files, contents = get_result(1, '11110', '201701')
    # print(json_files)
    # print(list(get_lawd_cd()).index('44200'))


