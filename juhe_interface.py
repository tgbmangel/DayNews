# -*- coding: utf-8 -*-
# @Project : DayNews 
# @Time    : 2018/11/5 14:16
# @Author  : 
# @File    : juhe_interface.py
# @Software: PyCharm
import requests

class JuHeApi():
    def __init__(self,api_url,interface_para_dict):
        '''
        聚合api初始化
        :param api_url: api的地址
        :param interface_para_dict:api的参数，包括key，作为dict传入
        '''
        self.api_url=api_url
        self.api_para=interface_para_dict
    def request_api(self,method):
        func=getattr(requests, method.lower())
        a = func(self.api_url, self.api_para)
        d = a.json()
        return d
    def parase_rsp(self,api_json):
        status=api_json.get('reason')
        result = api_json.get('result')

def get_wenxin_news():
    '''
    聚合api获取新闻
    :return:
    '''
    api_url='http://v.juhe.cn/weixin/query'
    method='POST'
    para={
        'pno':'',
        'ps':'',
        'dtype':'',
        'key':'fe0409f36554463a1c4583f1d443b351'
    }
    weixin_news=JuHeApi(api_url,para)
    rsp_json_dict=weixin_news.request_api(method)
    status=rsp_json_dict.get('reason')
    print(status)
    result=rsp_json_dict.get('result').get('list')
    if result:
        for res in result:
            title=res.get('title')
            source=res.get('source')
            img=res.get('firstImg')
            mark=res.get('mark')
            url=res.get('url')
            print(title,source,img,mark,'\n',url)
            print('----'*8)
    return result
def get_lottery(lottery_id)->str:
    '''
    获取彩票数据。
    :param lottery_id:彩票id（双色球：ssq，大乐透：dlt）
    :return: 本期彩票信息字符串
    '''
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
        strs +=f"开奖号码：↓↓\n【{result.get('lottery_res')}】\n"
        strs +=f"开奖日期：{result.get('lottery_date')}\n"
        strs +=f"兑奖过期日期：{result.get('lottery_exdate')}\n"
        strs +=f"本期销量：{result.get('lottery_sale_amount')}\n"
        strs +=f"奖池滚存：{result.get('lottery_pool_amount')}\n"
        prize=result.get('lottery_prize') #list
        # strs+='==========\n'
        if prize:
            for pr in prize:
                # strs+=f"{pr.get('prize_name')}{pr.get('prize_num')}注,单注:{pr.get('prize_amount')}元\n"
                pass
    return strs

def get_exp(com,no):
    '''
    通过聚合数据接口查询快递
    :param com:快递公司名称，获取快递简称用
    :param no:快递号
    :return:快递信息字符串
    '''
    exp_map={
        "顺丰":"sf",
        "申通":"sto",
        "圆通":"yt",
        "韵达":"yd",
        "天天":"tt",
        "EMS":"ems",
        "中通":"zto",
        "汇通":"ht",
    }
    com_cod=exp_map.get(com)
    if com_cod:
        api_url='http://v.juhe.cn/exp/index'
        p={
            'key':'58873cd58e4995104fcf3e402a141100',
            'com':com_cod,
            'no':no
        }
        strs=''
        a=requests.post(api_url,p)
        r=a.json()
        # strs+=f"{r.get('reason')}:\n"
        result=r.get('result')
        strs+=f'{result.get("company")} '
        strs +=f'{result.get("no")}\n'
        print(f'{result.get("status")}')
        exp_info=result.get('list')
        for _exp_info in exp_info:
            strs +=f"{_exp_info.get('datetime')},{_exp_info.get('remark')}\n"
        return strs
    else:
        return '未识别到快递公司，可能暂时不支持，也可能名称不匹配。'

def get_weather(cityname):
    api_url='http://v.juhe.cn/weather/index'
    para={
        'key':'2658deba9d1722c5b95c6bb4c35fedee',
        'cityname':cityname
    }
    method='get'
    weather = JuHeApi(api_url, para)
    rsp_json_dict = weather.request_api(method)
    status = rsp_json_dict.get('resultcode')
    print(status)
    result = rsp_json_dict.get('result')
    # print(result)
    sk=result.get('sk')
    for key,value in sk.items():
        print(key,':',value)
    print('---'*9)
    today=result.get('today')
    for key,value in today.items():
        print(key, ':', value)
    print('---'*9)


if __name__=='__main__':
    get_weather('长沙')