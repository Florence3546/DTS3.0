# coding=UTF-8


def get_paginator_bar(data_list):
    """
    :param data_list: 使用 django 的 Paginator 分割的单页数据
    :return: {'left': [], 'center': [], 'right': []}
    """
    pagi_bar = {'left': [], 'center': [], 'right': []}
    if data_list:
        if data_list.number < 5:
            pagi_bar['center'] = list(range(1, data_list.number + 1))
        else:
            pagi_bar['left'] = [1]
            pagi_bar['center'] = list(range(data_list.number - 2, data_list.number + 1))
        if data_list.paginator.num_pages - data_list.number < 4:
            pagi_bar['center'].extend(list(range(data_list.number + 1, data_list.paginator.num_pages + 1)))
        else:
            pagi_bar['center'].extend(list(range(data_list.number + 1, data_list.number + 3)))
            pagi_bar['right'] = [data_list.paginator.num_pages]
    return pagi_bar
