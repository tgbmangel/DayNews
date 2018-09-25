# -*- coding: utf-8 -*-
# @Project : DayNews 
# @Time    : 2018/9/20 10:25
# @Author  : 
# @File    : weiyu_sougou.py
# @Software: PyCharm
from requests_html import HTMLSession
import requests
import re

proxies = {
    "http": "http://111.155.124.78:8123",
    # 'http':'183.129.207.82:18118',
    'http':'123.207.66.68:3128',
    'http':'113.88.12.172:9000'
}

headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
}

sougouwenzhang_url='http://weixin.sogou.com/weixin?type=2&s_from=input&query=9%E6%9C%8825%E6%97%A5%E5%BE%AE%E8%AF%AD%E7%AE%80%E6%8A%A5&ie=utf8&_sug_=n&_sug_type_='
sougouwenzhang_url='http://weixin.sogou.com/weixin?type=2&s_from=input&query={}&ie=utf8&_sug_=n&_sug_type_='
key_word=u'9月25日微语简报'
# weiyu_url='https://mp.weixin.qq.com/s?src=11&timestamp=1537855092&ver=1143&signature=miLp2ckIcr3jJv*MiObvddzHzK9rw*MkENvUEUb4BFcx1aNnpjC8xjbqwqTGqLHSqWXYfHcNhAHUMeSaReeRTOc-m3h-7DFoqFPs-I9U26kWCY-cjHwPewspiLWrBoJ5&new=1'
s=HTMLSession()
r=s.get(sougouwenzhang_url.format(key_word))
htmls=r.html
divs=htmls.find('div.txt-box')
for div in divs:
    u,author=list(div.find('h3')[0].links)[0],div.find('div > a')[0].text
    if author=='微语简报':
        print('zhaodao')
# links=[x for x in r.html.links if x.endswith('new=1')]
# for link in links:
#     print(link)
# para_re=re.compile('window.sg_data=(.*)')
# src_re=re.compile('src:"(.*)"')
# ver_re=re.compile('ver:"(.*)"')
# timestamp_re=re.compile('timestamp:"(.*)"')
# signature_re=re.compile('signature:"(.*)"')
# signature=signature_re.findall(html_data)
# print(signature)
# links=r.html
# print(links)
#
# lin='http://mp.weixin.qq.com/s?src=11&timestamp=1537858579&ver=1143&signature=miLp2ckIcr3jJv*MiObvddzHzK9rw*MkENvUEUb4BFfkgRQwaBLMuo3DFCnEOHXCUKmFUdjMuXVC6wwPAervEd1ODfYZ3rbh10UaAGTNwaPa9qMzsbx3*bYk-t9JouiY&new=1'
# rr=s.get(links[0])
# # print(rr.html.html)
# # print(rr.html.find('#js_content > section:nth-child(5) > section')[0].text)
# print(rr.html.text)
