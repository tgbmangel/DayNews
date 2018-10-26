# -*- coding: utf-8 -*-
# @Project : DayNews 
# @Time    : 2018/10/25 14:13
# @Author  : 
# @File    : kuaidi_demos.py
# @Software: PyCharm
import requests

def get_exp(com,no):
    api_url='http://v.juhe.cn/exp/index'
    p={
        'key':'58873cd58e4995104fcf3e402a141100',
        'com':com,
        'no':no
    }
    strs=''
    a=requests.post(api_url,p)
    r=a.json()
    strs+=f"{r.get('reason')}:\n"
    result=r.get('result')
    strs+=f'{result.get("company")} '
    strs +=f'{result.get("no")}\n'
    print(f'{result.get("status")}')
    exp_info=result.get('list')
    for _exp_info in exp_info:
        strs +=f"{_exp_info.get('datetime')},{_exp_info.get('remark')}\n"
    return strs
if __name__=="__main__":
    print(get_exp('yd','3833224842423'))