# coding=UTF-8

import base64
import bz2
import inspect
import md5
import os
import urllib
import urllib2

import simplejson as json

from common.utils.utils_log import log


def url_param_2dict(query):
    '''
    \将URL参数列表转换为dict
    >>> url_param_2dict("aa=1&bb=222&cc=xyz")
    {'aa': '1', 'cc': 'xyz', 'bb': '222'}
    '''
    param_dict = {}
    for s in query.split('&'):
        if s.find('=') > -1:
            k, v = s[:s.find('=')], s[s.find('=') + 1:]
            param_dict[urllib.unquote(k)] = urllib.unquote(v)
        else:
            param_dict[s] = ''
    return param_dict

def make_sys_dir(the_dirs):
    '''逐级创建本地目录'''
    if not the_dirs:
        return False
    try:
        dir_str = ""
        if the_dirs.find("\\") != -1:
            the_dirs = the_dirs.replace("\\", "/")
        dir_list = the_dirs.split("/")
        for tmp_dir in dir_list:
            if tmp_dir:
                dir_str += tmp_dir + "/"
                if not os.path.exists(dir_str):
                    os.mkdir(dir_str)
    except Exception:
        return False
    return True

def read_txt_file(file_path):
    '''逐行读取本地txt文本文件'''
    if not file_path or not os.path.exists(file_path):
        log.error("file not exist, file_path=%s" % (file_path))
        return False

    try:
        file_r = open(file_path, 'r')
        data = file_r.readlines()
    except Exception, e:
        log.error("read file error, file_path=%s, e=%s" % (file_path, e))
        return False
    finally:
        if file_r:
            file_r.close()
    return data

def http_download_file(download_url, file_path, file_name = None):
    '''http下载远程文件，file_name非空，则file_path是存放目录，否则file_path还包含存放文件名'''
    if not download_url or not file_path:
        return False

    file_path = file_path.replace('\\', '/')
    dir_path = (file_name and file_path or file_path[0, file_path.rfind('/')])
    full_path = (file_name and (os.path.join(dir_path, file_name).replace('\\', '/')) or file_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    try:
        rf, wf = None, None
        req = urllib2.Request(download_url)
        rf = urllib2.urlopen(req)
        wf = open(full_path, 'w')
        wf.write(rf.read())
    except Exception, e:
        log.error("download file error, download_url=%s, file_path=%s, file_name=%s, e=%s" % (download_url, file_path, file_name, e))
        return False
    finally:
        if rf:
            rf.close()
        if wf:
            wf.close()
    return full_path

def verify_url_exist(url):
    '''
    \校验URL是否存在
    >>> verify_url_exist("http://www.baidu.com")
    True
    '''
    headers = {
        "Accept": "text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5",
        "Accept-Language": "en-us,en;q=0.5",
        "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.7",
        "Connection": "close",
        "User-Agent": 'ztcjl',
    }
    try:
        req = urllib2.Request(url, None, headers)
        urllib2.urlopen(req)
        return True
    except:
        return False

def get_request_ip(request):
    '''获取请求客户端的IP'''
    if request and request.META.has_key('HTTP_X_FORWARDED_FOR') and request.META['HTTP_X_FORWARDED_FOR']:
        # HTTP_X_FORWARDED_FOR can be a comma-separated list of IPs.Take just the first one.
        request_ip = request.META['HTTP_X_FORWARDED_FOR'].split(',')[0]
    elif request and request.META.has_key('REMOTE_ADDR'):
        request_ip = request.META['REMOTE_ADDR']
    else:
        request_ip = "127.0.0.1"
    return request_ip

def get_ip_area(ip):
    '''根据ip获取地域，要返回正确的地域在循环的list中加入相应的地名'''
    url = 'http://www.ip138.com/ips138.asp?ip=%s&action=2' % ip
    fd = urllib2.urlopen(url)
    s = fd.read()
    fd.close()
    us = s.decode('gb2312').encode('utf-8').replace('&nbsp;', '')
    ip_index = us.find('本站主数据：')
    addr = us[ip_index:ip_index + 100]
    for loc in ['武汉']:
        if loc in addr:
            return loc
    return ''

def get_idcard_info(userid):
    '''获取身份证相关信息'''
    data = [('action', 'idcard'), ('userid', '%s' % userid), ('B1', '查询'.decode('utf-8').encode('gb2312'))]
    query = urllib.urlencode(data)
    url = 'http://qq.ip138.com/idsearch/index.asp'
    req = urllib2.Request(url)
    fd = urllib2.urlopen(req, query)
    s = fd.read()
    fd.close()
    us = s.decode('gb2312').encode('utf-8').replace('&nbsp;', '')
    p_key = us.find('++* 查询结果 *++')
    p_start = us.find('<tr>', p_key, -1)
    p_end = us.find('</table>', p_key, -1)
    return us[p_start:p_end]


class Objectize(object):
    def __init__(self, **kwargs):
        if kwargs:
            for k, v in kwargs.items():
                setattr(self, k, v)

def set_value_with_secret(value, salt):
    """对需要加密的值进行加密，salt是密钥
    set_value_with_secret(1,'Hello')
    >>> "OGIxYTk5NTNjNDE2MTEyOTZhODI3YWJmOGM0NzgwNGQ3"
    """
    salt_md5 = md5.md5(salt).hexdigest()
    secret_str = '%s%s%s' % (salt_md5[:10], value, salt_md5[10:])
    return base64.encodestring(secret_str)

def get_value_with_secret(encrypted_value, salt):
    """对加密过的值进行解密，salt是密钥
    get_value_with_secret("OGIxYTk5NTNjNDE2MTEyOTZhODI3YWJmOGM0NzgwNGQ3",'Hello')
    >>> '1'
    """
    salt_md5 = md5.md5(salt).hexdigest()
    return base64.decodestring(encrypted_value).replace(salt_md5[:10], '').replace(salt_md5[10:], '')

def compress_obj(obj):
    """压缩，先转json，再用bz2压缩，470K能压缩成20多K"""
    temp_json = json.dumps(obj)
    return bz2.compress(temp_json)

def decompress_obj(compressed_str):
    """解压缩"""
    temp_json = bz2.decompress(compressed_str)
    return json.loads(temp_json)

def get_custom_attr(obj, data_str):
    """根据data_str中的属性字段返回对象中的属性值"""
    data_list = eval(data_str)
    json_data = {}
    for data in data_list:
        attr_list = data.split('.')
        last_attr = attr_list[-1]
        middle_attr = ''
        for m in attr_list[0:-1]:
            middle_attr += m
        first_obj = middle_attr and eval('obj.' + middle_attr) or obj
        key = data.replace('.', '_')
        if hasattr(first_obj, last_attr):
            json_data[key] = getattr(first_obj, last_attr)
    return json_data

def get_methods_8class(cls):
    method_dict = {}
    for k, v in cls.__dict__.iteritems():
        if k[:2] == '__': # 过滤掉 内部函数 如 __init__
            continue
        if inspect.isfunction(v): # 注意：__dict__ 中 使用 ismethod 是错误的
            method_dict.update({k: v.__doc__})
    return method_dict
