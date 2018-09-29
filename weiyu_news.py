# -*- coding: utf-8 -*-
# @Project : DayNews 
# @Time    : 2018/9/26 11:42
# @Author  : 
# @File    : weiyu_news.py
# @Software: PyCharm
import datetime
from requests_html import HTMLSession

def get_weiyu_news_today():
    headers = {
        'Host': 'weixin.sogou.com',
        'Refer':'http://weixin.sogou.com/weixin?type=2&query=9%E6%9C%8827%E6%97%A5%E5%BE%AE%E8%AF%AD%E7%AE%80%E6%8A%A5+%E6%98%9F%E6%9C%9F%E5%9B%9B&ie=utf8&s_from=input&_sug_=n&_sug_type_=1&w=01015002&oq=&ri=11&sourceid=sugg&sut=0&sst0=1538010259311&lkt=0%2C0%2C0&p=40040108',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    }

    day=datetime.datetime.now().day
    month=datetime.datetime.now().month
    week=datetime.date.weekday(datetime.datetime.now())
    # print(month,day,week)
    week_map={0:'一',1:'二',2:'三',3:'四',4:'五',5:'六',6:'天'}
    keyword=f'{month}月{day}日 微语简报 星期{week_map[week]} 微语简报'
    sougouwenzhang_url = 'http://weixin.sogou.com/weixin?type=2&s_from=input&query={}&ie=utf8&_sug_=n&_sug_type_='
    s = HTMLSession()
    print(sougouwenzhang_url.format(keyword))
    r = s.get(sougouwenzhang_url.format(keyword))
    htmls = r.html
    divs = htmls.find('div.txt-box')
    for div in divs:
        u, author = list(div.find('h3')[0].links)[0], div.find('div > a')[0].text
        print(u,author)
        if author == '微语简报':
            # print('zhaodao')
            rr=s.get(u)
            # print(rr.html.html)
            try:
                news_text=rr.html.find('#js_content')[0].text
                # '#js_content > section:nth-child(5) > p:nth-child(2)'
                print('获取到：',news_text)
                s.close()
                return news_text
            except Exception as e:
                pass
    s.close()

if __name__=='__main__':
    get_weiyu_news_today()