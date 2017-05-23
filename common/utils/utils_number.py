# coding=UTF-8
'''
数字对象(int、float、decimal等)处理工具类
Created on 2011-09-07
@author: zhangyu
'''

import math


def round_digit(src_data, digits = None):
    '''
    \四舍五入数字，并返回float类型。(python2.5、python2.7的round函数Bug较严重)
    src_data:数值或数字格式的字符串；digits:小数点位数，默认为2位，为负数则取绝对值
    \比如digits=2，则得到float(src_data+0.005+0.0001)后，再截取小数点后2位前面的字符串

    >>> round_digit(0.415,3)
    0.415
    >>> round_digit(0.415,2)
    0.42
    >>> round_digit("0.415490001", 3)
    0.416
    '''
    if src_data is None:
        return None
    try:
        if digits is None:
            digits = 2
        else:
            digits = int(math.fabs(digits))

        string_data = str(src_data)
        string_array = string_data.split(".")
        if len(string_array) == 2 and len(string_array[1]) > digits:
            tmp_data = str(float(string_data) + 5 * 10 ** -(digits + 1) + 1 * 10 ** -(digits + 2))
            tmp_array = tmp_data.split(".")
            if len(tmp_array) == 2 and len(tmp_array[1]) > digits:
                string_data = tmp_array[0] + "." + str(tmp_array[1][0:digits])
            else:
                string_data = tmp_data
        return float(string_data)
    except Exception:
        return None

def get_min_num(*a):
    tmp_list = []
    for num in a:
        if isinstance(num, (int, long, float)):
            tmp_list.append(num)
        else:
            return False
    tmp_list.sort()
    return tmp_list[0]

def clean_to_number(text):
    text = text.strip()
    if '.' in text:
        is_float = True
    else:
        is_float = False
    c_list = []
    for c in text:
        if c in '.1234567890':
            c_list.append(c)
        else:
            break

    text = ''.join(c_list)
    if not text:
        text = '0'
    if is_float:
        return float(text.replace(u'   ', u'.'))
    else:
        return int(text)

def clean_to_int(text):
    text = text.strip()
    c_list = []
    for c in text:
        if c in '1234567890':
            c_list.append(c)
        else:
            break
    text = ''.join(c_list)
    if not text:
        text = '0'
    return int(text)

def format_division(numerator, denominator, multiple = 100, point = '2'):
    '''
                方便计算，点击率，转化率，ppc等
    '''
    if numerator and denominator:
        return format(numerator * float(multiple) / denominator, '.' + point + 'f')
    else:
        return 0

def fen2yuan(v):
    return '%.2f' % (v/100.0)

def base10_to_baseN(x, n):
    '''n>2 and n<255'''
    s = ''
    top_c = int(math.log(x, n))
    for i in range(top_c):
        c, x = divmod(x, n ** (top_c - i))
        s += chr(c)
    s += chr(x)
    return s

def trans_price(price_str):
    """
    trans_price('192.00')
    >>> 19200
    """
    return int(float(price_str) * 100)

def doublestr_2int(str):
    return int(float(str))
