# -*- coding: utf-8 -*-
# @Project : DayNews 
# @Time    : 2018/10/30 16:20
# @Author  : 
# @File    : sougou_mp.py
# @Software: PyCharm
import datetime
from requests_html import HTMLSession
from log import logger
import re

def sougou_mp(se,name,code):
    '''
    #在微信搜索使用搜索公众号，获取公众号列表，然后找到 微语简报 的公众号
    se:se = HTMLSession()
    name=公众号名字
    code= 公众号
    :return: 公众号的url
    '''
    url='http://weixin.sogou.com/weixin?type=1&s_from=input&query={}&ie=utf8&_sug_=n&_sug_type_='
    key_word=name
    try:
        rsp=se.get(url.format(key_word))
        logger.info(url.format(key_word))
        #搜索公账号的结果div，包括所有结果
        div=rsp.html.find('#main > div.news-box')[0]
        lis=div.find('ul > li')
        for li in lis:
            links=li.links
            #微信号
            logger.info(li.find('p.info')[0].text)
            if li.find('p.info')[0].text == f'微信号：{code}':
                for link in links:
                    if link.startswith('http://mp.weixin.qq.com/profile?src=3'):
                        return link
    except Exception as e:
        logger.info(e)

def mp_articles(se,mp_url):
    '''
    :param se: se = HTMLSession()
    :param mp_url:
    :return:
    '''
    rp = se.get(mp_url)
    htmls = rp.html.html  # 文章html
    # print(htmls)
    # 获取msgList,在解析每篇文章的信息
    msg_list_patten = re.compile('var msgList = ({.+})')
    msg_list = re.findall(msg_list_patten, htmls)[0]
    msg_list = eval(msg_list)
    for x in msg_list.get('list'):
        # print('↓↓↓'*8)
        print(x)
        # 先获取文章的通用信息
        comm_msg_info = x.get('comm_msg_info')
        date_time = comm_msg_info.get('datetime')
        time_get = datetime.datetime.fromtimestamp(int(date_time))
        time_get_date = f'{time_get.year}-{time_get.month}-{time_get.day}'
        app_msg_ext_info = x.get('app_msg_ext_info')  # 文章的url、标题等，dict
        url_head = 'http://mp.weixin.qq.com'
        wenzhang_url = app_msg_ext_info.get('content_url')
        wenzhang_title = app_msg_ext_info.get('title')
        if not wenzhang_url:
            wenzhang_url = app_msg_ext_info.get('multi_app_msg_item_list')[0].get('content_url')
            wenzhang_title = app_msg_ext_info.get('multi_app_msg_item_list')[0].get('title')
        else:
            wenzhang_url = url_head + wenzhang_url
        print(wenzhang_url.replace('amp;', ''), wenzhang_title, time_get_date)
        logger.info(wenzhang_url.replace('amp;', '') + wenzhang_title + time_get_date)



if __name__=="__main__":
    se = HTMLSession()
    url=sougou_mp(se,'Steam社区','steamcommunity')
    mp_articles(se,url)
