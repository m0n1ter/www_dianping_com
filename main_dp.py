# -*- coding: utf-8 -*-
import sys
#sys.path.append('./dp')
sys.path.append(u'C:/Users/马超/Desktop/dp')
sys.path.append('./')
import shopid
import www_dianping_com as dianping
import pandas as pd



shid = shopid.shop_id(15080143)
page = shid.get_page_num()
ids = []
for i in range(1,page+1):
    ids = ids + shid.get_shop_id(i)
print(len(ids))



df = pd.DataFrame()
for i in ids:
    csi = dianping.class_shop_info()
    csi.get_shop_code(i)
    csi.get_basic_info()
    csi.get_score()
    csi.get_tag()
    df = df.append(csi.get_df())
    print(i)
df.to_csv(u'C:/Users/马超/Desktop/dp/通州.csv', index=False)




























