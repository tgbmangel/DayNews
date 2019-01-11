# -*- coding: utf-8 -*-
# @Project : DayNews 
# @Time    : 2018/10/26 16:33
# @Author  : zsr
# @File    : emoji_evil.py
# @Software: PyCharm
from log import logger
import chardet

def emoji_evil(input_string):
    '''
    处理特殊表情或者字符的（将特殊字符去掉）
    将接收到的字符串转为ascii，去掉emoji中以U000开头的编码字符
    然后将原ascii拼回去，转为utf8的编码，在反编码转为Unicode
    ==================================
    decode('unicode_escape') 是反编码：
    f='\u53eb\u6211'
    print f
    print(f.decode('unicode-escape'))
    >>\u53eb\u6211
    >>叫我
    ==================================
    :param input_string:
    :return:
    '''
    ascii_code=ascii(input_string)
    logger.info(f'emoji_evil ascii_code：{ascii_code}')
    _tmp_str=''
    if 'U000' in ascii_code:
        ascii_str_list = ascii_code.split('\'')[1].split('\\')
        for x in ascii_str_list:
            if 'U000' in x:
                pass
            elif not x:
                pass
            else:
                a = '\\{}'.format(x)
                _tmp_str=_tmp_str+a
        logger.info(f'emoji_evil _tmp_str：{_tmp_str}')
        logger.info(f'emoji_evil _tmp_str.encode("utf-8")：{_tmp_str.encode("utf-8")}')
        final_str=_tmp_str.encode('utf-8').decode('unicode_escape')
        logger.info(f'emoji_evil 转为final_str：{final_str}')
        return final_str
    elif 'u2005' in ascii_code:
        ascii_str_list = ascii_code.split('\'')[1].split('\\')
        for x in ascii_str_list:
            if 'u2005' in x:
                a = '\s'
                _tmp_str=_tmp_str+a
            elif not x:
                pass
            else:
                a = '\\{}'.format(x)
                _tmp_str=_tmp_str+a
        final_str=_tmp_str.encode('utf-8').decode('unicode_escape')
        logger.info(f'emoji_evil 转为：{final_str}')
        return final_str
    else:
        logger.info(f'emoji_evil 未转：{input_string}')
        return input_string