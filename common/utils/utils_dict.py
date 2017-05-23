# coding=UTF-8


class TempObject(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


def dict_2obj(dic):
    return TempObject(**dic)
