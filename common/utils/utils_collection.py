# coding=UTF-8
'''
集合对象(tuple、list、dict、set等)处理的工具类
Created on 2011-09-07
@author: zhangyu
'''
import math


def genr_sublist(org_list, slice_size):
    """
    >>> for temp_list in genr_sublist(range(20), 5):
            print temp_list

    [0, 1, 2, 3, 4]
    [5, 6, 7, 8, 9]
    [10, 11, 12, 13, 14]
    [15, 16, 17, 18, 19]
    """
    slice_count = int(math.ceil(len(org_list) / float(slice_size)))
    for i in xrange(slice_count):
        yield org_list[i * slice_size:(i + 1) * slice_size]

def query_string_2dict(data):
    """
    >>> query_string_2dict("a=1&b=2&c=3")
    {'a': '1', 'c': '3', 'b': '2'}
    >>> query_string_2dict("a=1&b=2$c=3")
    "is a Bug?"
    >>> query_string_2dict("a=1&a=2&a=3&b=2$c=3")
    "is a Bug?"
    """
    json = {}
    try:
        for eq in data.split("&"):
            parts = eq.split("=")
            if json.has_key(parts[0]):
                if isinstance(json[parts[0]], list):
                    json[parts[0]].append(parts[1])
                else:
                    json[parts[0]] = [json[parts[0]], parts[1]]
            else:
                json[parts[0]] = parts[1]
    except:
        pass
    return json

def range_to_list(_range):
    """
    >>> range_to_list("20-22;23-25")
    [20, 21, 22, 23, 24, 25]
    """
    try:
        lst = []
        for r in _range.split(';'):
            p1, p2 = r.split('-')
            step = int(p2) > int(p1) and 1 or -1
            lst += range(int(p1), int(p2) + step, step)
        lst.sort()
        return lst
    except:
        return []

def list_to_range(lst):
    '''
    >>> list_to_range([5])
    ''
    >>> list_to_range([1,5])
    '1-5'
    >>> list_to_range([1,5,10])
    "is a Bug?"
    '''
    try:
        if isinstance(lst, list):
            pass
        elif isinstance(lst, basestring):
            lst = eval(lst)
        lst.sort()
        if len(lst) < 2:
            return ''
        if len(lst) == 2:
            return '%s-%s' % (lst[0], lst[1])

        dot_lst = []
        for i in range(1, len(lst)):
            if lst[i] - lst[i - 1] > 1: # 把由跳跃的点都用dot_lst记下了
                dot_lst.append(i)
        dot_lst.insert(0, 0) # 把第0个，和最后一个加入dot_lst中
        dot_lst.append(len(lst)) # 这里不能减1

        rg_lst = []
        for i in range(1, len(dot_lst)):
            start_index = dot_lst[i - 1]
            end_index = dot_lst[i] - 1
            if end_index < start_index:
                end_index = start_index
            rg_lst.append("%s-%s" % (lst[start_index], lst[end_index]))
        return ';'.join(rg_lst)
    except:
        return ''

def list_to_string(src_list, dot = None):
    '''将一个list转换为以dot分隔的str'''
    if src_list:
        if not dot:
            dot = ","
        tmp_map = map(str, src_list)
        return dot.join(tmp_map)
    else:
        return ''

def split_list(large_list, split_number):
    '''将large_list分解成多个小组，每组个数为split_number个成员(最后一组除外)，返回组的队列
    >>> test_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    >>> split_list(test_list, 4)
    [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10]]
    >>> split_list(test_list, 5)
    [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]]
    >>> split_list(test_list, -1)
    [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]
    '''
    try:
        result_list = []
        list_lengh = len(large_list)

        if split_number <= 0 or list_lengh <= split_number:
            result_list.append(large_list[:])
        else:
            list_number = list_lengh / split_number
            if (list_lengh % split_number) != 0:
                list_number += 1 # 最后一组数据

            for i in range(list_number):
                temp_list = large_list[i * split_number:(split_number * (i + 1))]
                result_list.append(temp_list)
        return result_list
    except Exception:
        return []

def unicode_list_to_str_list(usl):
    '''字符串列表字符编码转换'''
    return ','.join(map(lambda x:"'%s'" % (x.encode('utf8')), usl))
