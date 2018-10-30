# -*- coding: utf-8 -*-
# @Project : DayNews 
# @Time    : 2018/9/26 11:42
# @Author  : 
# @File    : weiyu_news.py
# @Software: PyCharm
import datetime
from requests_html import HTMLSession
from log import logger
import time
import requests
import re

def get_weiyu_news_today():
    headers = {
        'Host': 'weixin.sogou.com',
        'Refer':'http://weixin.sogou.com/weixin?type=2&query=9%E6%9C%8827%E6%97%A5%E5%BE%AE%E8%AF%AD%E7%AE%80%E6%8A%A5+%E6%98%9F%E6%9C%9F%E5%9B%9B&ie=utf8&s_from=input&_sug_=n&_sug_type_=1&w=01015002&oq=&ri=11&sourceid=sugg&sut=0&sst0=1538010259311&lkt=0%2C0%2C0&p=40040108',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    }
    day=datetime.datetime.now().day
    month=datetime.datetime.now().month
    year=datetime.datetime.now().year
    week=datetime.date.weekday(datetime.datetime.now())
    today_str=f'{year}-{month}-{day}'
    # print(month,day,week)
    week_map={0:'一',1:'二',2:'三',3:'四',4:'五',5:'六',6:'天'}
    week_str=f'星期{week_map[week]}'
    keyword=f'{month}月{day}日 {week_str} 微语简报 '
    sougouwenzhang_url = 'http://weixin.sogou.com/weixin?type=2&s_from=input&query={}&ie=utf8&_sug_=n&_sug_type_='
    s = HTMLSession()
    print(sougouwenzhang_url.format(keyword))
    logger.info(sougouwenzhang_url.format(keyword))
    r = s.get(sougouwenzhang_url.format(keyword))
    htmls = r.html
    # print(htmls.html)
    divs = htmls.find('div.txt-box')
    for div in divs:
        u, author,time_str = list(div.find('h3')[0].links)[0], div.find('div > a')[0].text,div.find('div > span')[0].text
        print(time_str)
        time_get=datetime.datetime.fromtimestamp(int(time_str.split('\'')[1]))
        print(u,author,time_get)
        time_get_date=f'{time_get.year}-{time_get.month}-{time_get.day}'
        logger.info(f'{u},{author}{time_get.year,time_get.month,time_get.day}')
        if author == '微语简报'and today_str==time_get_date:
            # print('zhaodao')
            rr=s.get(u)
            # print(rr.html.html)
            try:
                # text_area=rr.html.find('#js_content')[0]
                news_text=rr.html.find('#js_content > section')[-1].text
                # '#js_content > section:nth-child(5) > p:nth-child(2)'
                print('获取到：',news_text)
                logger.info(news_text)
                s.close()
                return news_text
            except Exception as e:
                logger.info(e)
                pass
    s.close()

def weiyu_news_p_account():
    '''
    #在微信搜索使用搜索公众号，获取公众号列表，然后找到 微语简报 的公众号
    进入公众号页面，获取文章列表，然后找到对应日期（当天的）文章地址
    进入当天文章，获取文章text
    :return: 文章内容
    '''
    url='http://weixin.sogou.com/weixin?type=1&s_from=input&query={}&ie=utf8&_sug_=n&_sug_type_='
    key_word='微语简报'
    #日期
    day = datetime.datetime.now().day
    month = datetime.datetime.now().month
    year = datetime.datetime.now().year
    week = datetime.date.weekday(datetime.datetime.now())
    today_str = f'{year}-{month}-{day}'
    # print(month,day,week)
    week_map = {0: '一', 1: '二', 2: '三', 3: '四', 4: '五', 5: '六', 6: '天'}
    week_str = f'星期{week_map[week]}'
    se=HTMLSession()
    rsp=se.get(url.format(key_word))
    logger.info(url.format(key_word))
    #搜索公账号的结果div，包括所有结果
    div=rsp.html.find('#main > div.news-box')[0]
    lis=div.find('ul > li')
    for li in lis:
        links=li.links
        #微信号
        logger.info(li.find('p.info')[0].text)
        if li.find('p.info')[0].text=='微信号：weiyunews':
            for link in links:
                if link.startswith('http://mp.weixin.qq.com/profile?src=3'):
                    #公众号链接
                    logger.info(link)
                    #请求公众号页面，进入到公众号所有文章的页面。
                    rp=se.get(link)
                    htmls=rp.html.html#文章html
                    # print(htmls)
                    #获取msgList,在解析每篇文章的信息
                    msg_list_patten=re.compile('var msgList = ({.+})')
                    msg_list=re.findall(msg_list_patten,htmls)[0]
                    msg_list=eval(msg_list)
                    for x in msg_list.get('list'):
                        # print('↓↓↓'*8)
                        # print(x)
                        #先获取文章的通用信息，通过时间来判断是不是今天的文章
                        comm_msg_info=x.get('comm_msg_info')
                        date_time=comm_msg_info.get('datetime')
                        time_get = datetime.datetime.fromtimestamp(int(date_time))
                        time_get_date = f'{time_get.year}-{time_get.month}-{time_get.day}'
                        if time_get_date==today_str:
                            app_msg_ext_info = x.get('app_msg_ext_info')  # 文章的url、标题等，dict
                            url_head='http://mp.weixin.qq.com'
                            wenzhang_url=app_msg_ext_info.get('content_url')
                            wenzhang_title=app_msg_ext_info.get('title')
                            if not wenzhang_url:
                                wenzhang_url=app_msg_ext_info.get('multi_app_msg_item_list')[0].get('content_url')
                                wenzhang_title=app_msg_ext_info.get('multi_app_msg_item_list')[0].get('title')
                            else:
                                wenzhang_url=url_head+wenzhang_url
                            print(wenzhang_url.replace('amp;',''),wenzhang_title,time_get_date)
                            logger.info(wenzhang_url.replace('amp;', '')+wenzhang_title+time_get_date)
                            if '微语简报' in wenzhang_title:
                                # return wenzhang_url.replace('amp;',''),wenzhang_title,time_get_date
                                try:
                                    rp=se.get(wenzhang_url.replace('amp;',''))
                                    news_text = rp.html.find('#js_content > section')[-1].text
                                    print('获取到：', news_text)
                                    logger.info(news_text)
                                    se.close()
                                    return news_text
                                except Exception as e:
                                    logger.info(e)
                                    pass

def get_lottery(lottery_id):
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

    :param com:
    :param no:
    :return:
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

if __name__=='__main__':
    print(get_exp("韵达",'3833224842423'))