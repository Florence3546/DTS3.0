# -*- coding: utf-8 -*-
import random
from captcha.conf import settings
from django.core.urlresolvers import reverse
from six import u, text_type

from captcha.models import CaptchaStore
from common.utils.utils_sms import send_sms



def random_char_challenge():
    """随机字符串"""
    chars, ret = u('abcdefghijklmnopqrstuvwxyz'), u('')
    for i in range(settings.CAPTCHA_LENGTH):
        ret += random.choice(chars)
    return ret.upper(), ret


def random_number_challenge():
    """随机数字"""
    chars, ret = u('1234567890'), u('')
    for i in range(settings.CAPTCHA_LENGTH):
        ret += random.choice(chars)
    return ret


def make_sms():
    """生成短信号码"""
    random_number = random_number_challenge()
    # TODO by liuhuan 2017-3-24 msg抽离
    text = '来自派生科技的验证码'
    msg = text + str(random_number)
    return msg, random_number