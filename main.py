# -*- coding: utf-8 -*-
# @Project : DayNews 
# @Time    : 2018/9/19 9:33
# @Author  : 
# @File    : main.py
# @Software: PyCharm

import time
import schedule
import itchat
import threading
from weiyu_news import *
from log import logger

def get_chatroom_username(room_name):
    try:
        chatroomUserName=itchat.search_chatrooms(room_name)[0]['UserName']
        return  chatroomUserName
    except Exception as e:
        return

def send_message_chatroom_news(chat_room):
    '''
    定时任务
    '''
    print('send_message_chatroom')
    qun_user_name=get_chatroom_username(chat_room)
    if qun_user_name:
        logger.info(qun_user_name)
        message = get_weiyu_news_today()
        logger.info(message)
        itchat.send(message,toUserName=get_chatroom_username(chat_room))
    else:
        logger.info('未获取到群username')

def send_message_chatroom_para(chat_room,message):
    '''
    定时任务
    '''
    logger.info('send_message_chatroom_para')
    # chat_room = '经济研讨'
    qun_user_name=get_chatroom_username(chat_room)
    if qun_user_name:
        logger.info(qun_user_name)
        message_send='{} {}'.format(time.strftime('%H:%M',time.localtime()),message)
        logger.info(message_send)
        itchat.send(message_send,toUserName=get_chatroom_username(chat_room))
    else:
        logger.info('未获取到群username')

@itchat.msg_register(itchat.content.TEXT,isGroupChat=True)
def print_msg(msg):
    logger.info(msg.text)
    if msg.text=='新闻呢' or msg.text=='新闻呢？':
        logger.info('收到指令')
        news=get_weiyu_news_today()
        if news:
            msg.user.send(news)
        else:
            msg.user.send('新闻又炸了。')

def schedule_send():
    logger.info('start time:{}'.format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())))
    while True:
        schedule.run_pending()
        logger.info('schedule_send...{}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
        time.sleep(20)

if __name__=='__main__':
    itchat.auto_login(hotReload=True)
    schedule.every().day.at("7:00").do(send_message_chatroom_news,'经济研讨')
    schedule.every().day.at("9:40").do(send_message_chatroom_news,'上山打老虎')
    schedule.every().day.at("17:29").do(send_message_chatroom_para,'经济研讨','群提醒：准备下班咯！有的大佬已经下班咯。')
    t=threading.Thread(target=schedule_send)
    t.start()
    itchat.run()