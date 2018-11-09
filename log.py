# -*- coding: utf-8 -*-
# @Project : upupup 
# @Time    : 2018/9/18 16:43
# @Author  : 
# @File    : logs.py
# @Software: PyCharm
import logging
import logging.handlers
import datetime
logger = logging.getLogger(__name__)
logger.setLevel(level = logging.DEBUG)
# handler = logging.FileHandler("logs/news.log",encoding='utf-8')
handler =logging.handlers.TimedRotatingFileHandler(
    "logs/news.log",
    encoding='utf-8',
    when='midnight',
    interval=1,
    backupCount=7,
    atTime=datetime.time(0, 0, 0, 0)
)
formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s')
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
stream_handler=logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(handler)
logger.addHandler(stream_handler)