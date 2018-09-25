# -*- coding: utf-8 -*-
# @Project : DayNews 
# @Time    : 2018/9/19 9:33
# @Author  : 
# @File    : main.py
# @Software: PyCharm
from requests_html import HTMLSession
import datetime
import time
import schedule
import itchat
import threading

def main():
    url='https://mp.weixin.qq.com/s/oeiYjgCaA27jYhe47n1RnA'
    ses=HTMLSession()
    r=ses.get(url)
    # r=requests.get(url)
    print(r.html.html)

def get_chatroom_username(room_name):
    try:
        chatroomUserName=itchat.search_chatrooms(room_name)[0]['UserName']
        return  chatroomUserName
    except Exception as e:
        return

def send_message_chatroom():
    '''
    定时任务
    '''
    print('send_message_chatroom')
    chat_room = '经济研讨'
    qun_user_name=get_chatroom_username(chat_room)
    if qun_user_name:
        print(qun_user_name)
        message = get_weiyu_news_today()
        itchat.send(message,toUserName=get_chatroom_username(chat_room))
    else:
        print('未获取到群username')

def schedule_send():
    print('start time:{}'.format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())))
    while True:
        schedule.run_pending()
        # print(itchat.check_login())
        print('schedule_send...')
        time.sleep(20)


def get_weiyu_news_today():
    day=datetime.datetime.now().day
    month=datetime.datetime.now().month
    week=datetime.date.weekday(datetime.datetime.now())
    # print(month,day,week)
    week_map={0:'一',1:'二',2:'三',3:'四',4:'五',5:'六',6:'天'}
    keyword=f'{month}月{day}日微语简报 星期{week_map[week]}'
    sougouwenzhang_url = 'http://weixin.sogou.com/weixin?type=2&s_from=input&query={}&ie=utf8&_sug_=n&_sug_type_='
    s = HTMLSession()
    r = s.get(sougouwenzhang_url.format(keyword))
    htmls = r.html
    divs = htmls.find('div.txt-box')
    for div in divs:
        u, author = list(div.find('h3')[0].links)[0], div.find('div > a')[0].text
        # print(u,author)
        if author == '微语简报':
            # print('zhaodao')
            rr=s.get(u)
            # print(rr.html.html)
            try:
                news_text=rr.html.find('#js_content > section:nth-child(5) > section')[0].text
                print(news_text)
                return news_text
            except Exception as e:
                pass

@itchat.msg_register(itchat.content.SHARING)
def print_msg(msg):
    print(msg.text)

if __name__=='__main__':
    itchat.auto_login(hotReload=True)
    # schedule.every(2).minutes.do(send_message_chatroom)

    # chat_room = '经济研讨'
    schedule.every().day.at("07:00").do(send_message_chatroom)
    # schedule.every().day.at("17:40").do(send_message_chatroom,chat_room,'群提醒：{}准备下班咯！'.format(time.strftime("%Y%m%d %H:%M:%S",time.localtime())))
    t=threading.Thread(target=schedule_send)
    t.start()
    itchat.run()