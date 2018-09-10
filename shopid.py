# -*- coding: utf-8 -*-
import json
import requests
from urllib.parse import urlencode
#import time
from json import JSONDecodeError
import sys
sys.path.append(u'C:/Users/马超/Desktop/dp')
sys.path.append('./')
import proxy_dianping
from bs4 import BeautifulSoup
import faker


f = faker.Faker(locale='zh_cn')


class shop_id:

    def __init__(self, plaza_code):
        self.h = {'User-Agent':f.user_agent()}       
        self.random_ip = proxy_dianping.get_an_ip()
        self.plaza_code = plaza_code
        self.bs = ''
        self.error_code = '抱歉！页面暂时无法访问......\n\n                \n去大众点评首页\n\n'


    def __repr__(self):
        return 'ip:{}, \n万达广场:{}'.format(self.random_ip['http'],self.plaza_code)


    def connect(self, url):
        try:
            r = requests.get(url, timeout=5, headers=self.h, proxies = self.random_ip)
            self.bs = BeautifulSoup(r.text, 'lxml')
            return self.bs
        except (requests.exceptions.RequestException, JSONDecodeError):
            return self.connect(url)


    def get_page_num(self):
        data = {'mallid':self.plaza_code,
                'latitude':0,
                'longitude':0,
                'utm_source':'',
                'query':2-0,
                'page':1,
                'pagesize':50,
                }
        url='https://mapi.dianping.com/shopping/mall/shops?' + urlencode(data)
        try:
            r = requests.get(url, timeout=5, headers=self.h, proxies = self.random_ip)
            page = json.loads(r.text)['msg']['totalCount']
            if page%50 != 0:
                page = int(page/50)+1
            else:
                page = page/50
            return page
        except (requests.exceptions.RequestException, JSONDecodeError):
            return self.page_num()


    def get_shop_id(self, page):
        data = {'mallid':self.plaza_code,
                'latitude':0,
                'longitude':0,
                'utm_source':'',
                'query':2-0,
                'page':page,
                'pagesize':50,
                }   
        url='https://mapi.dianping.com/shopping/mall/shops?' + urlencode(data)
        try:
            r = requests.get(url, timeout=5, headers=self.h, proxies = self.random_ip)
            shop_list = json.loads(r.text)['msg']['shops']
            shopid_list = [i['shopId'] for i in shop_list]
            return shopid_list
        except (requests.exceptions.RequestException, JSONDecodeError):
            return self.shop_info(page)




if __name__ == '__main__':
    shopid = shop_id(32400780)
    page = shopid.get_page_num()
    ids = []
    for i in range(1,page+1):
        ids = ids + shopid.get_shop_id(i)








