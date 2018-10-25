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
from itchat.content import *
from weiyu_news import *
from log import logger
import re

yun=itchat.new_instance()
def get_chatroom_username(room_name):
    try:
        chatroomUserName=yun.search_chatrooms(room_name)[0]['UserName']
        return  chatroomUserName
    except Exception as e:
        return

def unicode_nickname(input_string):
    '''
    处理特殊表情或者字符的（将特殊字符去掉）
    :param input_string:
    :return:
    '''
    strrr=ascii(input_string)
    b=''
    if 'U000' in strrr:
        str_list = strrr.split('\'')[1].split('\\')
        for x in str_list:
            if 'U000' in x:
                pass
            elif not x:
                pass
            else:
                a = '\\{}'.format(x)
                b=b+a
        final_str=b.encode('utf-8').decode('unicode_escape')
        return final_str
    elif 'u2005' in strrr:
        str_list = strrr.split('\'')[1].split('\\')
        for x in str_list:
            if 'u2005' in x:
                a = '\s'
                b=b+a
            elif not x:
                pass
            else:
                a = '\\{}'.format(x)
                b=b+a
        final_str=b.encode('utf-8').decode('unicode_escape')
        return final_str
    else:
        return input_string

def send_message_chatroom_news(chat_room):
    '''
    定时任务
    '''
    print('send_message_chatroom_news')
    qun_user_name=get_chatroom_username(chat_room)
    if qun_user_name:
        logger.info(qun_user_name)
        message = get_weiyu_news_today()
        if not message:
            message='新闻又炸了！'
        logger.info(message)
        yun.send(message,toUserName=get_chatroom_username(chat_room))
    else:
        logger.info('未获取到群username')

def send_message_chatroom_lottery(chat_room):
    '''
    定时任务
    '''
    print('send_message_chatroom_lottery')
    qun_user_name=get_chatroom_username(chat_room)
    if qun_user_name:
        logger.info(qun_user_name)
        message = get_lottery()
        if not message:
            message='彩票又炸了！'
        logger.info(message)
        yun.send(message,toUserName=get_chatroom_username(chat_room))
    else:
        logger.info('未获取到群username')

def send_message_chatroom_exp(chat_room,new_type,*para):
    '''
    定时任务
    '''
    print('send_message_chatroom_exp')
    qun_user_name=get_chatroom_username(chat_room)
    if qun_user_name:
        if new_type=='exp':
            com,no=para
            logger.info(qun_user_name)
            message = get_exp(com,no)
            if not message:
                message='快递接口无返回'
            logger.info(message)
            yun.send(message,toUserName=get_chatroom_username(chat_room))
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
        yun.send(message_send,toUserName=get_chatroom_username(chat_room))
    else:
        logger.info('未获取到群username')

news_keywords=['新闻呢','新闻呢？','新闻']
lottery_keywords=['彩票','双色球']
exp_keywords='查快递'
@yun.msg_register([TEXT,SHARING,CARD],isGroupChat=True)
def print_msg(msg):
    try:
        logger.info(unicode_nickname(msg['User']['NickName']))
    except Exception as e:
        logger.info(e)
    logger.info(msg.type)
    logger.info(msg['MsgType'])
    try:
        logger.info('{}:{}'.format(unicode_nickname(msg['ActualNickName']),unicode_nickname(msg.content)))
    except Exception as e:
        logger.info(e)
    # logger.info(msg.text)
    if msg.text in news_keywords:
        logger.info('收到指令')
        news=get_weiyu_news_today()
        if news:
            msg.user.send(news)
        else:
            msg.user.send('新闻又炸了。')
            logger.info('新闻又炸了。')
    elif msg.text in lottery_keywords:
        logger.info(f'收到指令：{msg.text}')
        lottery=get_lottery()
        if lottery:
            msg.user.send(lottery)
        else:
            msg.user.send('彩票炸了。')
            logger.info('彩票炸了。')
    elif msg.text.startswith(exp_keywords):
        logger.info(f'收到指令：{msg.text}')
        _msg_get=re.split('[，。,.\- +\s\t]',msg.text[3:])
        _msg_get = [x for x in _msg_get if not x == '']
        com,no,*_=_msg_get
        lottery=get_exp(com,no)
        if lottery:
            msg.user.send(lottery)
        else:
            msg.user.send('快递炸了。')
            logger.info('快递炸了。')
    if msg.text =='share':
        share='<?xml version="1.0"?>\n<msg>\n\t<appmsg appid="" sdkver="0">\n\t\t<title>湖南人文科技学院2006级同学聚会</title>\n\t\t<des>湖南人文科技学院2006级同学聚会</des>\n\t\t<action />\n\t\t<type>5</type>\n\t\t<showtype>0</showtype>\n\t\t<soundtype>0</soundtype>\n\t\t<mediatagname />\n\t\t<messageext />\n\t\t<messageaction />\n\t\t<content />\n\t\t<contentattr>0</contentattr>\n\t\t<url>http://u8906416.viewer.maka.im/k/6JFDVCXP</url>\n\t\t<lowurl />\n\t\t<dataurl />\n\t\t<lowdataurl />\n\t\t<appattach>\n\t\t\t<totallen>0</totallen>\n\t\t\t<attachid />\n\t\t\t<emoticonmd5 />\n\t\t\t<fileext />\n\t\t\t<cdnthumburl>3059020100045230500201000204aa862d7402033d14ba0204358ffa3a02045bacaa64042b777875706c6f61645f3232373732393030304063686174726f6f6d32343636375f313533383034323436380204010800030201000400</cdnthumburl>\n\t\t\t<cdnthumbmd5>9d8429811f5a6555d3f4fff98f7076f9</cdnthumbmd5>\n\t\t\t<cdnthumblength>8896</cdnthumblength>\n\t\t\t<cdnthumbwidth>160</cdnthumbwidth>\n\t\t\t<cdnthumbheight>160</cdnthumbheight>\n\t\t\t<cdnthumbaeskey>f408b5904d8145089668b44e900c47c0</cdnthumbaeskey>\n\t\t\t<aeskey>f408b5904d8145089668b44e900c47c0</aeskey>\n\t\t\t<encryver>0</encryver>\n\t\t\t<filekey>5038605309@chatroom50_1538105855</filekey>\n\t\t</appattach>\n\t\t<extinfo />\n\t\t<sourceusername />\n\t\t<sourcedisplayname />\n\t\t<thumburl>http://img1.maka.im/user/2331742/images/2312effa3a3279f7c318550afdcc36c1.png@0-7-349-349a_100w</thumburl>\n\t\t<md5 />\n\t\t<statextstr />\n\t\t<webviewshared>\n\t\t\t<jsAppId>wx63a2b3814c822ef7</jsAppId>\n\t\t</webviewshared>\n\t</appmsg>\n\t<fromusername></fromusername>\n\t<scene>0</scene>\n\t<appinfo>\n\t\t<version>1</version>\n\t\t<appname></appname>\n\t</appinfo>\n\t<commenturl></commenturl>\n</msg>\n'
        # yun.send_raw_msg(49,share,'filehelper')
        # msg.user.send('http://u8906416.viewer.maka.im/k/6JFDVCXP')
        pass
    if msg['MsgType']==49 or msg['MsgType']==42:
        logger.info('49 get')
        logger.info(type(msg['Content']))
        # itchat.send_raw_msg(msg['MsgType'], msg['Content'],'filehelper')

def schedule_send():
    logger.info('start time:{}'.format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())))
    while True:
        schedule.run_pending()
        logger.info('schedule_send...{}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
        time.sleep(28)

if __name__=='__main__':
    yun.auto_login(hotReload=True)
    schedule.every().day.at("7:00").do(send_message_chatroom_news,'经济研讨')
    schedule.every().day.at("9:40").do(send_message_chatroom_news,'上山打老虎')
    schedule.every().monday.at("18:00").do(send_message_chatroom_para,'经济研讨','群提醒：准备下班咯！有的大佬已经下班咯。')
    schedule.every().tuesday.at("18:00").do(send_message_chatroom_para,'经济研讨','群提醒：准备下班咯！有的大佬已经下班咯。')
    schedule.every().tuesday.at("21:59").do(send_message_chatroom_lottery,'经济研讨')
    schedule.every().wednesday.at("18:00").do(send_message_chatroom_para,'经济研讨','群提醒：准备下班咯！有的大佬已经下班咯。')
    schedule.every().thursday.at("18:00").do(send_message_chatroom_para,'经济研讨','群提醒：准备下班咯！有的大佬已经下班咯。')
    schedule.every().thursday.at("21:59").do(send_message_chatroom_lottery,'经济研讨')
    schedule.every().friday.at("18:00").do(send_message_chatroom_para,'经济研讨','群提醒：准备下班咯！有的大佬开启周末假期咯。')
    schedule.every().saturday.at("18:00").do(send_message_chatroom_para,'经济研讨','群提醒：周六加班的大佬可以下班了！')
    schedule.every().sunday.at("21:59").do(send_message_chatroom_lottery, '经济研讨')
    # schedule.every().saturday.at("8:00").do(send_message_chatroom_para,'经济研讨','[群提醒]鸡哥定制：单反中的照片。')
    t=threading.Thread(target=schedule_send)
    t.start()
    try:
        yun.run()
    except Exception as e:
        logger.info(e)
