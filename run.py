# -*- coding: utf-8 -*-
# @Project : DayNews 
# @Time    : 2018/10/26 14:20
# @Author  : 
# @File    : run.py
# @Software: PyCharm

from daydayup import *
from main import yun
from log import logger
import threading
#TODO 解决多文件调用关系(目前调用main.py里面的都没有用上)

if __name__=="__main__":
    yun.auto_login(hotReload=True)
    #新闻
    add_schedule('send_message_chatroom_news','day','7:00','经济研讨')
    add_schedule('send_message_chatroom_news','day','7:00','上山打老虎')
    # add_schedule('send_message_chatroom_para','day','14:30','朱家群','[奸笑]')
    #每日下班发送策略
    add_week_schedule('send_message_chatroom_para','1234',"18:00",'经济研讨','群提醒：准备下班咯！有的大佬已经下班咯。')
    add_week_schedule('send_message_chatroom_para','5',"18:00",'经济研讨','群提醒：准备下班咯！有的大佬开启周末假期咯。')
    add_week_schedule('send_message_chatroom_para','6',"18:00",'经济研讨','群提醒：周六加班的大佬可以下班了！')
    #彩票定时发送策略
    send_time="21:59"
    chat_room='经济研讨'
    add_week_schedule('send_message_chatroom_lottery','136',send_time,chat_room,'dlt')
    add_week_schedule('send_message_chatroom_lottery','247',send_time,chat_room,'ssq')
    #定时任务一直循环
    t=threading.Thread(target=schedule_send)
    t.start()
    #启动itchat保持登录。
    try:
        yun.run()
    except Exception as e:
        logger.info(e)
