from typing import Collection
import requests
from pprint import pprint
import json
from pymongo import MongoClient


def get_url(page_num, how_many):
    URL = "https://data.gm.go.kr/openapi/Apttradedelngdetail"
    API_KEY = "2668956ec64c4d05a9a9fbce8e605fe9"

    params = f"?KEY={API_KEY}&Type=json&pIndex={page_num}&pSize={how_many}"
    full_url = URL + params

    req = requests.get(full_url)    
    data = req.json()
    print(req.status_code)
    return data

def extract_data(data, page_num):
    sales_data = data['Apttradedelngdetail'][1]['row']

    with open(f'./My_apt/real_estate_json/apt_{page_num}.json', 'w') as json_file:
        for data in sales_data:
            json.dump(data, json_file)

    return sales_data

def connect_mongo():
    username = "ruo"
    password = "160813"
    URI = f"mongodb+srv://{username}:{password}@cluster0.yisdq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    client = MongoClient(URI)
    return client

def insert_data(client, json_files, page_num):
    my_db = client['Real_Estate']
    coll_name = 'GwangMyung_Apt_Sales'
    my_coll = my_db[coll_name]
    if page_num == 1:
        my_coll.drop()
    my_coll.insert_many(json_files)

def load_data_to_mongo():
    client = connect_mongo()
    for i in range(1, 26):
        json_data = get_url(i, 1000)
        sales_data = extract_data(json_data, i)
        insert_data(client, sales_data, i)

if __name__ == '__main__':
    load_data_to_mongo()