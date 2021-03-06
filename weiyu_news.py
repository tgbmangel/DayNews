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
import re
import urllib
import os

def cbk(a, b, c):
    '''
    下载回调函数
    :param a:
    :param b:
    :param c:
    :return:
    '''
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
    print('%.2f%%' % per)

def get_news_text(s,u,date_time):
    '''
    :param s: HTMLSession
    :param u: 文章url
    :return: 新闻文章内容
    '''
    news_text_local=f'news/{date_time}.txt'
    news_img_local=f'news/{date_time}.jpg'
    if os.path.exists(news_text_local):
        logger.info('存在文字版')
        print('存在文字版')
        with open(news_text_local,'r',encoding='utf8') as f:
            news_text=f.read()
            if news_text:
                print('read news_text:',news_text)
                return news_text
    elif os.path.exists(news_img_local):
        logger.info('存在图片版')
        print('存在图片版')
        news_text=news_img_local
        return news_text
    else:
        logger.info('本地没有新闻文件')
        print('本地没有新闻文件')
        try:
            rr = s.get(u)
            news_text = ''
            _news_text = rr.html.find('#js_content')[-1]
            print('_news_text',_news_text)
            news_text_p=_news_text.find('p')
            for p in news_text_p:
                if p.text:
                    if not '就是微语简报。' in p.text:
                        news_text+=f'{p.text}\n'
            # '#js_content > section:nth-child(5) > p:nth-child(2)'
            if news_text:
                news_compile = re.compile(r'.*\n+')
                a = news_compile.findall(news_text)
                all_text=list(a)
                tag='一份微语报'
                _idx=1
                for idx,v in enumerate(all_text):
                    if tag in v:
                        _idx=idx
                news_slice=slice(_idx-1,_idx+14)
                news_text=''.join(all_text[news_slice])
                print('get news_text：',news_text)
                with open(news_text_local, 'wt',encoding='utf8') as f:
                    f.write(news_text)
                print('获取到文字版：', news_text)
                logger.info(news_text)
            if news_text=='':
                news_text_img=_news_text.find('p > img')[0]
                print('news_text_img',news_text_img)
                img_url=news_text_img.attrs['data-src']
                urllib.request.urlretrieve(img_url, news_img_local, cbk)
                print(f'获取到图片：{news_img_local}')
                news_text=news_img_local
            return news_text
        except Exception as e:
            print('Exception:',e)
            logger.info(e)
            return

def get_weiyu_news_today():
    logger.info('get_weiyu_news_today')
    print('get_weiyu_news_today')
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
            return get_news_text(s,u,today_str)

    s.close()

def weiyu_news_p_account():
    '''
    #在微信搜索使用搜索公众号，获取公众号列表，然后找到 微语简报 的公众号
    进入公众号页面，获取文章列表，然后找到对应日期（当天的）文章地址
    进入当天文章，获取文章text
    :return: 文章内容
    '''
    logger.info('weiyu_news_p_account')
    print('weiyu_news_p_account')
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
        # print(li.find('p.info')[0].text,links)
        if li.find('p.info')[0].text=='微信号：weiyunews':
            for link in links:
                print(link)
                if link.startswith('http://mp.weixin.qq.com/profile?src=3'):
                    #公众号链接
                    logger.info(link)
                    print(link,'对上了')
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
                        print('msg_list',x)
                        #先获取文章的通用信息，通过时间来判断是不是今天的文章
                        comm_msg_info=x.get('comm_msg_info')
                        date_time=comm_msg_info.get('datetime')
                        time_get = datetime.datetime.fromtimestamp(int(date_time))
                        time_get_date = f'{time_get.year}-{time_get.month}-{time_get.day}'
                        if time_get_date==today_str:
                        # if time_get_date=='2018-10-29':
                            app_msg_ext_info = x.get('app_msg_ext_info')  # 文章的url、标题等，dict
                            url_head='http://mp.weixin.qq.com'
                            wenzhang_url=app_msg_ext_info.get('content_url')
                            wenzhang_title=app_msg_ext_info.get('title')
                            if not '微语简报' in wenzhang_title:
                                wenzhang_url=app_msg_ext_info.get('multi_app_msg_item_list')[0].get('content_url')
                                wenzhang_title=app_msg_ext_info.get('multi_app_msg_item_list')[0].get('title')
                            wenzhang_url = url_head + wenzhang_url
                            print('文章的信息：',wenzhang_url.replace('amp;',''),wenzhang_title,time_get_date)
                            logger.info(wenzhang_url.replace('amp;', '')+wenzhang_title+time_get_date)
                            if not url_head==wenzhang_url:
                                news_url=wenzhang_url.replace('amp;','')
                                return get_news_text(se, news_url, today_str)
                            else:
                                return
                        else:
                            continue
    se.close()



if __name__=='__main__':
    # print(get_exp("韵达",'3833224842423'))
    weiyu_news_p_account()