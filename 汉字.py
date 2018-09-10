# -*- coding: utf-8 -*-
import requests
import faker
import re
from bs4 import BeautifulSoup
import json

f = faker.Faker(locale='zh_cn')
h = {'User-Agent':f.user_agent(),}




url='http://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/shoptextcss/textcss.GdumTHUA96.css'
r = requests.get(url,headers=h)
r.text
fr = re.findall('(fr-[a-zA-Z0-9]{4})',r.text)


url='http://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/shoptextcss/review.GdumTHUA96.svg'
r = requests.get(url,headers=h)
bs = BeautifulSoup(r.text,'lxml')
hanzi = []
for i in bs.findAll('text'):
    hanzi = hanzi + re.findall('.',i.text)

fr_hanzi = dict(zip(fr,hanzi))



def x(i):
    return '<span class="{}"></span>'.format(i)

zz=[]
for i in map(x,fr_hanzi.keys()):
    zz.append(i)



fr_hanzi = dict(zip(zz,hanzi))














with open(u'C:\\Users\马超\\Desktop\\dp\\fr', "w",encoding='utf-8') as f:  
    json.dump(fr_hanzi, f)



with open(u'C:\\Users\马超\\Desktop\\dp\\fr','r',encoding='utf-8') as f:
    print(f)
    sd = json.load(f)











