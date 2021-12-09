import sqlite3
from pymongo import MongoClient
from realestate_api import connect_mongo

def connection_sqlite():
    conn = sqlite3.connect('./My_apt/apt_sale.db')
    cur = conn.cursor()
    return conn, cur

def create_table():
    conn, cur = connection_sqlite()
    cur.execute("DROP TABLE IF EXISTS apt_sales;")
    cur.execute("""CREATE TABLE apt_sales (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        YEAR VARCHAR,
        SALES INTEGER,
        LEGALDONG_LOTNO_CD VARCHAR,
        LEGALDONG_EMD_TYPE_CD VARCHAR,
        LEGALDONG_SIGNGU_TYPE_CD VARCHAR,
        LEGALDONG_VICENO_TYPE_CD VARCHAR,
        LEGALDONG_ORIGNO_TYPE_CD VARCHAR,
        LEGALDONG_NM VARCHAR,
        ROADNM_DIV_CD VARCHAR,
        ROADNM_GROUND_UNDGRND_CD VARCHAR,
        ROADNM_SN_TYPE_CD VARCHAR,
        ROADNM_SIGNGU_TYPE_CD VARCHAR,
        ROADNM_BULDNG_VICENO_TYPE_CD VARCHAR,
        ROADNM_BULDNG_ORIGNO_TYPE_CD VARCHAR,
        ROADNM VARCHAR,
        FLOOR_CNT INTEGER,
        LOTNO INTEGER,
        MANAGE_NO VARCHAR,
        APT_NM VARCHAR,
        BUILD_YY VARCHAR,
        DATE VARCHAR,
        MONTH VARCHAR,
        PRVTUSE_AR FLOAT
    );""")
    conn.commit()
    return conn, cur

def get_json_from_mongodb():
    client = connect_mongo()
    my_db = client['Real_Estate']
    coll_name = 'GwangMyung_Apt_Sales'
    my_coll = my_db[coll_name]
    data = my_coll.find()
    return data

def insert_json_to_sqlite():
    conn, cur = create_table()
    data = get_json_from_mongodb()
    for json_file in data:
        cur.execute("""INSERT INTO apt_sales 
        (
            'YEAR', 'SALES', 'LEGALDONG_LOTNO_CD', 
        'LEGALDONG_EMD_TYPE_CD', 'LEGALDONG_SIGNGU_TYPE_CD', 
        'LEGALDONG_VICENO_TYPE_CD', 'LEGALDONG_ORIGNO_TYPE_CD', 
        'LEGALDONG_NM', 'ROADNM_DIV_CD', 'ROADNM_GROUND_UNDGRND_CD', 
        'ROADNM_SN_TYPE_CD', 'ROADNM_SIGNGU_TYPE_CD', 
        'ROADNM_BULDNG_VICENO_TYPE_CD', 'ROADNM_BULDNG_ORIGNO_TYPE_CD', 
        'ROADNM', 'FLOOR_CNT', 'LOTNO', 'MANAGE_NO', 'APT_NM', 'BUILD_YY', 
        'DATE', 'MONTH', 'PRVTUSE_AR'
        ) 
        VALUES 
        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (json_file['YY'], json_file['DELNG_AMT'], 
        json_file['LEGALDONG_LOTNO_CD'], 
        json_file['LEGALDONG_EMD_TYPE_CD'], json_file['LEGALDONG_SIGNGU_TYPE_CD'], 
        json_file['LEGALDONG_VICENO_TYPE_CD'], json_file['LEGALDONG_ORIGNO_TYPE_CD'], 
        json_file['LEGALDONG_NM'], json_file['ROADNM_DIV_CD'], 
        json_file['ROADNM_GROUND_UNDGRND_CD'], 
        json_file['ROADNM_SN_TYPE_CD'], json_file['ROADNM_SIGNGU_TYPE_CD'], 
        json_file['ROADNM_BULDNG_VICENO_TYPE_CD'], 
        json_file['ROADNM_BULDNG_ORIGNO_TYPE_CD'], 
        json_file['ROADNM'], json_file['FLOOR_CNT'], json_file['LOTNO'], 
        json_file['MANAGE_NO'], json_file['APT_NM'], json_file['BUILD_YY'], 
        json_file['DE'], json_file['MT'], json_file['PRVTUSE_AR']))
    conn.commit()

if __name__ == '__main__':
    insert_json_to_sqlite()