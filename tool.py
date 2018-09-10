# -*- coding: utf-8 -*-
import json





with open(u'C:\\Users\马超\\Desktop\\dp\\fr','r',encoding='utf-8') as f:
    fr_cn = json.load(f)



def replace_fr(x):
    if x != None:
        for k,v in fr_cn.items():
            x = x.replace(k, str(v))
        return x
    else:
        return 'null'




def replace_score(x): 
    data_score={'<span class="fn-urRy"></span>':0,
                '<span class="fn-FJy9"></span>':2,
                '<span class="fn-huhQ"></span>':3,
                '<span class="fn-3Ywa"></span>':4,
                '<span class="fn-Ws1o"></span>':5,
                '<span class="fn-xfkY"></span>':6,
                '<span class="fn-zpQd"></span>':7,
                '<span class="fn-0lrK"></span>':8,
                '<span class="fn-04ho"></span>':9,
                }
    if x != None:
        for k,v in data_score.items():
            x = x.replace(k,str(v))
        return x
    else:
        return 'null'




def list_to_dict(dic):
    if dic != '':
        keys=dic.keys()
        vals=dic.values()
        L=[key+':'+val for key,val in zip(keys,vals)]
        return ','.join(L)
    else:
        return ''




def list_to_str(l):
    if l == None:
        return ''
    else:
        ','.join(l)








if __name__ == '__main__':
    replace_score()
    map(replace_score, '1')
    replace_score(None)








