# -*- coding: utf-8 -*-
# @Project : DayNews 
# @Time    : 2018/9/26 11:37
# @Author  : 
# @File    : daydayup.py
# @Software: PyCharm
import schedule
from log import logger
import time
from main import *

def add_schedule(func_name,way,action_time,*para):
    '''
    :param func_name: 调用的函数名
    :param way:schedule.every() 的方法：day,monday...
    :param action_time:执行时间
    :param para:函数func_name的名称
    :return:schedule的执行任务
    '''
    func=globals().get(func_name)
    print(func.__name__)
    sc=schedule.every()
    way_fun=getattr(sc,way)
    way_fun.at(action_time).do(globals().get(func_name),*para)

def add_week_schedule(func_name,way,action_time,*para):
    '''
    按week来封装
    :param func_name:
    :param way: '1' -周一，'12':周一和周二，‘13’周一和周三,只识别1到6
    :param action_time:
    :param para:
    :return:
    '''
    week_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    way_list=[int(x)-1 for x in way if int(x)>0 if int(x)<8]
    week_daysss=[week_days[x] for x in way_list]
    for wk in week_daysss:
        print(func_name,wk,action_time,*para)
        add_schedule(func_name,wk,action_time,*para)

def schedule_send():
    logger.info('start time:{}'.format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())))
    while True:
        schedule.run_pending()
        logger.info('schedule_send...{}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
        time.sleep(28)

