# coding=UTF-8

import urllib
import urllib2

from django.conf import settings

from common.utils.utils_log import log

alarm_count = 0
def inform_boss(func):
    """发送短信后，如果余额不足，就知会boss"""

    def _check(*args, **kwargs):
        global alarm_count
        result = func(*args, **kwargs)
        if 'tmoney' in result and result['tmoney'] < 50:
            if alarm_count % 100 == 0:
                alarm_count += 1
                func([settings.SMS_BOSS_PHONE], content = '短信平台余额仅剩：%s' % result['tmoney'])
            else:
                alarm_count = 0
        return result
    return _check

@inform_boss
def send_sms(receiver_list, content):

    def parse_result(org_str):
        """
        >>>parse_result('000/Send:1/Consumption:.08/Tmoney:301/sid:0305154306719405')
        {'tmoney': 301, 'code': 0, 'consumption': 0.08, 'send': 1, 'sid': '0305154306719405'}
        """
        s = 'code:' + org_str.lower()
        lst = s.split('/')
        if len(lst) != 5:
            return {}
        result = {}
        for i in lst:
            t = i.split(':')
            if len(t) != 2:
                return {}
            try:
                result[t[0]] = eval(t[1])
            except:
                result[t[0]] = t[1]
        return result

    result = {}
    if not settings.SMSABLE:
        return
    else:
        request_data = [('id', '%s' % settings.SMS_USERID.decode('utf-8').encode('gb2312')),
                        ('pwd', '%s' % settings.SMS_PASSWORD),
                        ('to', '%s' % ','.join(map(str, receiver_list))),
                        ('content', '%s' % content.decode('utf-8').encode('gb2312')),
                        ('time', '')]
        request_data = urllib.urlencode(request_data)
        url = 'http://service.winic.org/sys_port/gateway/'
        req = urllib2.Request(url)
        response = urllib2.urlopen(req, request_data)
        log.debug('SMS requested: %s |||||| %s' % (url, request_data))
        result = response.read()
        response.close()
        log.debug('SMS responsed: %s' % result)

    return parse_result(result)
