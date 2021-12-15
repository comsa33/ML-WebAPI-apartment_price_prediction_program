import sqlite3
from pymongo import MongoClient
from realestate_all_api import connect_mongo

def connection_sqlite():
    conn = sqlite3.connect('./My_apt/apt_sale.db')
    cur = conn.cursor()
    return conn, cur

def create_table():
    conn, cur = connection_sqlite()
    cur.execute("DROP TABLE IF EXISTS all_apt_sales;")
    cur.execute("""CREATE TABLE all_apt_sales (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        SALES VARCHAR,
        BUILD_YY VARCHAR,
        YEAR VARCHAR,
        ROADNM VARCHAR,
        LEGALDONG_NM VARCHAR,
        APT_NM VARCHAR,
        MONTH VARCHAR,
        DATE VARCHAR,
        MANAGE_NO VARCHAR,
        PRVTUSE_AR VARCHAR,
        FLOOR_CNT VARCHAR,
        CODE VARCHAR
    );""")
    conn.commit()
    return conn, cur

def get_json_from_mongodb():
    client = connect_mongo()
    my_db = client['Real_Estate']
    coll_name = 'Apt_Sales'
    my_coll = my_db[coll_name]
    data = my_coll.find()
    return data

def insert_json_to_sqlite():
    conn, cur = create_table()
    data = get_json_from_mongodb()
    for json_file in data:
        try:
            cur.execute("""INSERT INTO all_apt_sales 
            (
            'SALES','BUILD_YY','YEAR','ROADNM','LEGALDONG_NM',
            'APT_NM','MONTH','DATE','MANAGE_NO','PRVTUSE_AR', 'FLOOR_CNT', 'CODE' 
            ) 
            VALUES 
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (json_file['거래금액'], json_file['건축년도'], 
            json_file['년'], 
            json_file['도로명'], json_file['법정동'], 
            json_file['아파트'], json_file['월'], 
            json_file['일'], json_file['일련번호'], 
            json_file['전용면적'], 
            json_file['층'], json_file['지역코드']))
        except:
            pass
    conn.commit()

def get_valid_code():
    conn, cur = connection_sqlite()
    code = cur.execute("""
    SELECT DISTINCT aas.CODE 
    FROM all_apt_sales aas""")
    code = code.fetchall()
    code = [x[0] for x in code]
    return code

if __name__ == '__main__':
    insert_json_to_sqlite()
    # data = get_json_from_mongodb()
    # print(data['도로명'])
    