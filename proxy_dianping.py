# -*- coding: utf-8 -*-
import requests
import re
import json
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from json import JSONDecodeError



h = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36 LBBROWSER'}


def get_89ip():
    url = 'http://www.89ip.cn/tqdl.html?api=1&num=1000&port=&address=&isp='
    r = requests.get(url, timeout=5, headers=h)
    ip_89ip = re.findall('<br>(.*?)<br>',r.text)
    return ip_89ip

def check_ip(proxy):
    proxy_data = {'http':'http://'+str(proxy)}
    try:
        s = requests.get(url='https://mapi.dianping.com/searchshop.json?start=0&categoryid=508&parentCategoryId=10&locatecityid=0&limit=50&sortid=2&cityid=2&range=-1&maptype=0&regionid=1475',
#                         url='https://m.dianping.com/shop/67145735',
                         headers=h,
                         proxies = proxy_data,
                         timeout=3)
        if s.status_code == 200:
            json.loads(s.text)
            print(proxy)
            return proxy
        else:
            print(proxy,' -- 403')
            return np.NAN
    except (Exception, JSONDecodeError):
        print(proxy,' -- 403')
        return np.NAN

def into_db(ips, append_replace):
    df = pd.DataFrame(ips, columns=['ip'])
    df.drop_duplicates(inplace=True)
    df.dropna(axis = 0, how = 'any', inplace=True)
    sql = 'postgresql+pg8000://postgres:dd1314@localhost:5432/weatherdata'
    conn = create_engine(sql, encoding='utf8')
    pd.io.sql.to_sql(df, 'proxy', conn,
                     if_exists = append_replace,
                     index = False, 
                     chunksize = 2000)

def get_an_ip():
    conn_sql = 'postgresql+pg8000://postgres:dd1314@localhost:5432/weatherdata'
    conn = create_engine(conn_sql,encoding='utf8')
    sql = 'SELECT * FROM proxy ORDER BY RANDOM() LIMIT 1;'
    df = pd.read_sql(sql,conn)
    return {'http':'http://'+list(df['ip'])[0]}


def delete_an_ip(i):   
    conn_sql = 'postgresql+pg8000://postgres:dd1314@localhost:5432/weatherdata'
    conn = create_engine(conn_sql,encoding='utf8')
    sql = 'DELETE FROM proxy WHERE ip={!r};'.format(i)
    conn.execute(sql)


def check_db_ip():
    conn_sql = 'postgresql+pg8000://postgres:dd1314@localhost:5432/weatherdata'
    conn = create_engine(conn_sql,encoding='utf8')
    sql = 'SELECT * FROM proxy;'
    df = pd.read_sql(sql,conn)
    df.drop_duplicates(inplace=True)
    df.dropna(axis = 0, how = 'any', inplace=True)
    ips = [check_ip(i) for i in df['ip']]
    ips = ips[0:1000]
    into_db(ips,'replace')





if __name__ == "__main__":
    ip_89ip = get_89ip()
    ips = [check_ip(i) for i in ip_89ip]
    into_db(ips,'append')
    get_an_ip()
    check_db_ip()











