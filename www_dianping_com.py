# -*- coding: utf-8 -*-
import json
import requests
from urllib.parse import urlencode
from json import JSONDecodeError
import sys
sys.path.append(u'C:/Users/马超/Desktop/dp')
sys.path.append('./')
#import proxy_dianping
import pandas as pd
import tool
import faker

f = faker.Faker(locale='zh_cn')

class class_shop_info():

    def __init__(self):
        self.h = {'User-Agent':f.user_agent(),
                  'Cookie':'_lxsdk_cuid=163a5f09f01c8-07ea3286706a42-2b6f686a-1fa400-163a5f09f01c8; _hc.v=3ac0d73e-88e1-5f0c-01ee-f3714262a552.1527497400; ctu=4a5ac28ee0552d2a11bce90adfcf4f5fc90ede926b0f028c059f283be2949ca1; switchcityflashtoast=1; yl_tg=8; cityid=2; _tr.u=cTG967g3KOPs4zbk; Hm_lvt_e6f449471d3527d58c46e24efb4c343e=1535328749; aburl=1; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; cy=2; cye=beijing; s_ViewType=10; _lxsdk=0CFB9A30AF2011E8A7BE6928DC19DF06579928A4A70C4E04B0CA7FBBC2DA79F5; source=m_browser_test_22; pvhistory="6L+U5ZuePjo8L3NzbmV3P2tleXdvcmQ9JUU3JTgxJUFCJUU1JUFFJUI0JUU1JUIxJUIxJUU2JTk2JUIwJUU3JTk2JTg2JUU4JThGJTlDJUU2JTlEJUE1JUU0JUJBJTg2KCVFNCVCOCU4NyVFOCVCRSVCRSVFNSVCOSVCRiVFNSU5QyVCQSVFNSVCQSU5NykmXz0xNTM1OTQ0OTA2NTIwJmNhbGxiYWNrPVplcHRvMTUzNTk0NDg4MzIwNj46PDE1MzU5NDQ5MDk3MzJdX1s="; m_flash2=1; msource=default; default_ab=citylist%3AA%3A1%7Cshop%3AA%3A1%7Cindex%3AA%3A1%7CshopList%3AA%3A1%7Cshopreviewlist%3AA%3A1%7Cmap%3AA%3A1%7Csinglereview%3AA%3A1; lgtoken=06f23e881-ae1e-4f4b-8255-c283b6bb80bc; dper=00851b418f3d9d4e2bb33366fd84263f8aebcf7e55d7029060e9f7b74348c5e42d4c89072413470e7d68152839fb0bfe12eecc119c5563a8331ff1a5c7fca2ac1cf16599bab20be43e2bf138773d1eb78bfb9b4c3973814773dda0dcbf21e463; ll=7fd06e815b796be3df069dec7836c3df; ua=12312341234; _lxsdk_s=1659df09909-9b1-17d-6c2%7C%7C138'}
        self.shopid = ''
        self.cityid = ''
        self.maincategoryid = ''
        self.shoptype = ''
        self.shop_info = {}
    
    def __repr__(self):
        s = 'shopid: {}\ncityid: {}\nmaincategoryid: {}\nshoptype: {}'
        return s.format(self.shopid, self.cityid, self.maincategoryid, self.shoptype)


    def get_shop_code(self, shopid):
        self.shopid = shopid
        url='http://www.dianping.com/ajax/json/shopDynamic/shopAside?shopId={}'.format(self.shopid)
        try:
            r = requests.get(url,timeout=5,headers=self.h)
            self.maincategoryid = json.loads(r.text)['category']['mainParentCategoryId']
            self.cityid = json.loads(r.text)['city']['cityID']
            self.shoptype = json.loads(r.text)['shop']['shopType']
            self.shop_info['mainParentCategoryId'] = self.maincategoryid
        except (requests.exceptions.RequestException, JSONDecodeError) as e:
            self.get_shop_code(shopid)


    def get_basic_info(self):
        url='http://www.dianping.com/ajax/json/shopDynamic/basicHideInfo?shopId=' + str(self.shopid)
        try:
            r = requests.get(url,timeout=5,headers=self.h)
            self.shop_info['shopId'] = json.loads(r.text)['msg']['shopInfo']['shopId']
            self.shop_info['shopType'] = json.loads(r.text)['msg']['shopInfo']['shopType']
            self.shop_info['shopName'] = json.loads(r.text)['msg']['shopInfo']['shopName']
            self.shop_info['branchName'] = json.loads(r.text)['msg']['shopInfo']['branchName']
            self.shop_info['phoneNo'] = json.loads(r.text)['msg']['shopInfo']['phoneNo']
            self.shop_info['phoneNo2'] = json.loads(r.text)['msg']['shopInfo']['phoneNo2']
            self.shop_info['cityId'] = json.loads(r.text)['msg']['shopInfo']['cityId']
            self.shop_info['shopGroupId'] = json.loads(r.text)['msg']['shopInfo']['shopGroupId']
            self.shop_info['altName'] = json.loads(r.text)['msg']['shopInfo']['altName']
            self.shop_info['businessHours'] = json.loads(r.text)['msg']['shopInfo']['businessHours']
        except (requests.exceptions.RequestException, JSONDecodeError):
            self.get_basic_info()


    def get_score(self):
        data={'shopId':self.shopid,
              'cityId':self.cityid,
              'mainCategoryId':self.maincategoryid,
              }
        url='http://www.dianping.com/ajax/json/shopDynamic/reviewAndStar?'+urlencode(data)
        try:
            r = requests.get(url,timeout=5,headers=self.h)
            score = json.loads(r.text)
            if score['shopRefinedScoreValueList'] != None:
                list_score = [x for x in map(tool.replace_score, score['shopRefinedScoreValueList'])]
                self.shop_info['score'] = dict(zip(score['shopScoreTitleList'], list_score))
            else:
                self.shop_info['score'] = ''
            self.shop_info['avgPrice'] = tool.replace_score(score['avgPrice'])
            self.shop_info['score4'] = score['score4']
            self.shop_info['defaultReviewCount'] = score['defaultReviewCount']
            self.shop_info['shopPower'] = score['shopPower']
            self.shop_info['code'] = score['code']
        except (requests.exceptions.RequestException, JSONDecodeError):
            self.get_score()


    def get_tag(self):
        data={'shopId':self.shopid,
              'cityId':self.cityid,
              'shopType':self.shoptype,
              }
        url='http://www.dianping.com/ajax/json/shopDynamic/allReview?'+urlencode(data)
        try:
            r = requests.get(url,timeout=5,headers=self.h)
            review = json.loads(r.text)
            if review['msg'] != '政府相关商户':
                self.shop_info['dishTagStrList'] = tool.list_to_str(review['dishTagStrList'])
                shop_tag = {}
                if review['summarys'] != None:
                    for i in review['summarys']:
                        shop_tag[i['summaryString']]=str(i['summaryCount'])
                    self.shop_info['tag'] = shop_tag
                else:
                    self.shop_info['tag'] = ''
            else:
                self.shop_info['dishTagStrList'] = ''
                self.shop_info['tag'] = ''
        except (requests.exceptions.RequestException, JSONDecodeError):
            self.get_tag()


    def get_df(self):
        self.shop_info['score'] = tool.list_to_dict(self.shop_info['score'])
        self.shop_info['tag'] = tool.list_to_dict(self.shop_info['tag'])
        df = pd.DataFrame.from_dict(self.shop_info,orient='index').T
        return df


if __name__ == '__main__':
    
    csi = class_shop_info()
    csi.get_shop_code(72406553)
    csi.get_basic_info()
    csi.get_score()
    csi.get_tag()

    df = pd.DataFrame()
    df = df.append(csi.get_df())
    adf = csi.shop_info







