# -*- coding: utf-8 -*-
# @Project : upupup 
# @Time    : 2018/9/18 16:43
# @Author  : 
# @File    : log.py
# @Software: PyCharm
import logging
logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler("news.log",encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s')
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
logger.addHandler(handler)