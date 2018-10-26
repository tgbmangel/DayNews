# -*- coding: utf-8 -*-
# @Project : DayNews 
# @Time    : 2018/10/25 10:19
# @Author  : 
# @File    : caipiao.py
# @Software: PyCharm

import requests
import json

def get_lottery():
    api_url = 'http://apis.juhe.cn/lottery/query'
    data = {
        'key': 'd7ce4c0b11f2a0d48a309df093d23412',
        'lottery_id': 'ssq'
    }
    a = requests.post(api_url, data)
    d=a.json()
    print(d)
    print(type(d))
    strs=''
    if d.get('reason')=='查询成功':
        result=d.get('result')
        strs += f"第{result.get('lottery_no')}期 "
        strs+=f"{result.get('lottery_name')}\n"
        strs +=f"开奖号码：{result.get('lottery_res')}\n"
        strs +=f"开奖日期：{result.get('lottery_date')}\n"
        strs +=f"兑奖过期日期：{result.get('lottery_exdate')}\n"
        strs +=f"本期销量：{result.get('lottery_sale_amount')}\n"
        strs +=f"奖池滚存：{result.get('lottery_pool_amount')}\n"
        prize=result.get('lottery_prize') #list
        strs+='==========\n'
        if prize:
            for pr in prize:
                strs+=f"{pr.get('prize_name')},中奖注数:{pr.get('prize_num')},单注金额:{pr.get('prize_amount')},中奖规则:{pr.get('prize_require')}\n"
    return strs
def get_lottery_dlt(lottery_id):
    api_url = 'http://apis.juhe.cn/lottery/query'
    data = {
        'key': 'd7ce4c0b11f2a0d48a309df093d23412',
        'lottery_id': lottery_id
    }
    a = requests.post(api_url, data)
    d=a.json()
    print(d)
    print(type(d))
    strs=''
    if d.get('reason')=='查询成功':
        result=d.get('result')
        strs += f"第{result.get('lottery_no')}期 "
        strs+=f"{result.get('lottery_name')}\n"
        strs +=f"开奖号码：{result.get('lottery_res')}\n"
        strs +=f"开奖日期：{result.get('lottery_date')}\n"
        strs +=f"兑奖过期日期：{result.get('lottery_exdate')}\n"
        strs +=f"本期销量：{result.get('lottery_sale_amount')}\n"
        strs +=f"奖池滚存：{result.get('lottery_pool_amount')}\n"
        prize=result.get('lottery_prize') #list
        strs+='==========\n'
        if prize:
            for pr in prize:
                strs+=f"{pr.get('prize_name')},中奖注数:{pr.get('prize_num')},单注金额:{pr.get('prize_amount')},中奖规则:{pr.get('prize_require')}\n"
    return strs

if __name__=="__main__":
    print(get_lottery_dlt('dlt'))
