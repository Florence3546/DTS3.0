# coding=UTF-8
'''
字符处理的工具类
Created on 2011-09-07
@author: zhangyu
'''

import random
import urllib
from slugify import slugify


def escape_special_keyword(the_str):
    '''处理关键词中包含的特殊字符'''
    if the_str:
        if the_str.find("\\") != -1:
            the_str = the_str.replace("\\", r"\\")
        if the_str.find("'") != -1:
            the_str = the_str.replace("'", r"\'")
        if the_str.find('"') != -1:
            the_str = the_str.strip('"')
        if the_str.find(',') != -1:
            the_str = the_str.replace(',', r' ')
        if the_str.find('[') != -1:
            the_str = the_str.replace('[', r'')
        if the_str.find(']') != -1:
            the_str = the_str.replace(']', r'')
    return the_str


def get_random_string(length = 8):
    '''获取指定长度的随机数字字符串'''
    return ''.join([str(random.randint(0, 9)) for i in range(length)])


def get_utf8_string(the_str):
    '''将字符串编码格式由unicode转换为utf-8'''
    if isinstance(the_str, unicode):
        return the_str.encode("utf-8")
    else:
        return str(the_str)


def escape_url(the_str, safe = '~'):
    '''转换URL中的特使字符，标记为safe的char不转换'''
    return urllib.quote(the_str, safe = safe)


def get_char_num(the_str):
    the_str = unicode(the_str)
    count = 0
    for cc in the_str:
        if ord(cc) <= 127:
            count += 0.5
        else:
            count += 1
    return count


def get_part_word_num(the_str):
    '''计算分词的个数，根据空格来计算'''
    str_list = the_str.split(' ')
    count = 0
    for temp in str_list:
        if temp:
            count += 1
        else:
            continue
    return count


def is_duplicate_word(str1, str2):
    '''
    \是否是重复词判断

    \重复词主要包括以下分类：
    1，顺序颠倒，如“韩版 连衣裙”与“连衣裙 韩版”
    2，空格有否，如“韩版 连衣裙”与“韩版连衣裙”
    3，淘宝判定的同义词，如“女士”、“女式”、“女款”均是重复词
    \这里只作前二者的判断，第三类不作处理
    '''
    tmp_str1 = str1.replace(' ', '')
    tmp_str2 = str2.replace(' ', '')
    if len(tmp_str1) == len(tmp_str2):
        if set(tmp_str1) == set(tmp_str2):
            return True
    return False


def check_duplicate_word(the_str, words_set):
    '''检查是否是重负词，words_set形如：[(set(' ','u\505f','u\987e'),5),(set(' ','u\5a5d','u\987f'),7)]'''
    if not words_set:
        return False
    tmp_str = the_str.replace(' ', '')
    tmp_set = set(tmp_str)
    for word in words_set:
        if len(tmp_str) == word[1] and tmp_set == word[0]:
            return True
    return False


def get_word_set(the_str):
    tmp_str1 = the_str.replace(' ', '')
    return ''.join(set(tmp_str1))


def get_ordered_str(the_str):
    if u'的' in the_str:
        the_str = the_str.replace(u'的', '')
    return ''.join(sorted(list(the_str.replace(' ', ''))))


def get_pinyin_code(text):
    """获取拼音码"""
    pinyin = slugify(text)
    return ''.join([word[0].upper() for word in pinyin.split('-') if word])
