# coding=UTF-8
import time
import os

from django.conf import settings
from django.template import Library
from django.utils.safestring import mark_safe
from django.db.models import Q

from common.utils.utils_log import log
from common.constant import NAV_URL_DICT
from django.template import Library, Node, TemplateSyntaxError

register = Library()


def div(value, arg): # arg：分子字段名、分母字段名、小数点位数、放大倍数；以逗号分开。
    '''
    usage:
    {{value|div:'x,y'}}
    {{value|div:'x,y,2'}}
    {{value|div:'x,y,2,100'}}
    '''
    try:
        args = arg.split(',')
        f_bit = 2
        times = 1
        if len(args) > 2:
            f_bit = args[2]
        if len(args) > 3:
            times = float(args[3])

        fmt = '%%0.%sf' % (f_bit)
        if args[0].isdigit():
            v0 = float(args[0])
        else:
            if '.' in args[0]:
                attr1, attr2 = args[0].split('.')
                if isinstance(value, dict):
                    v0 = float(value[attr1].__dict__[attr2])
                else:
                    v0 = float(getattr(value, attr1).__dict__[attr2])
            else:
                if isinstance(value, dict):
                    v0 = float(value[args[0]])
                else:
                    v0 = float(getattr(value, args[0]))
        if args[1].isdigit():
            v1 = float(args[1])
        else:
            if '.' in args[1]:
                attr1, attr2 = args[1].split('.')
                if isinstance(value, dict):
                    v1 = float(value[attr1].__dict__[attr2])
                else:
                    v1 = float(getattr(value, attr1).__dict__[attr2])
            else:
                if isinstance(value, dict):
                    v1 = float(value[args[1]])
                else:
                    v1 = float(getattr(value, args[1]))
        if v0 and v1:
            return fmt % (v0 / v1 * times)
        else:
            return 0
    except:
        return 0
register.filter(div)

def sort_column(value):
    # 因为table_sort是按字符串来排序的，导致20大于100。所以在20前面补0。
    try:
        if value:
            return mark_safe('<span class="hide">%012.2f</span>%s' % (float(value), value))
        else:
            return value
    except Exception, e:
        log.exception("sort_column(value=%s) raise error=%s" % (value, e))
        return mark_safe('<span class="hide">%s</span>%s' % (value, value))
register.filter(sort_column)

def sum_list(value):
    if type(value) == type([]):
        return str(sum(value))
    else:
        try:
            tmp = eval(value)
        except:
            tmp = []
        return str(sum(tmp))
register.filter(sum_list)

def left_list(value):
    '''
            将传过来的实时数据按当前时间截断，去掉后面的0
            比如现在是上午8点多，那么将截断：
    [1,2,3,1,3,0,2,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]->[1,2,3,1,3,0,2,3,0]
    '''
    try:
        hour = int(time.strftime('%H'))
        return value[:hour + 1]
    except:
        return value
register.filter(left_list)

def kw_decode(value):
    # 替换传过来的字符串的相关字符
    try:
        return value.replace('+', ' ')
    except:
        return value
register.filter_function(kw_decode)

def divide(value, args):
    """
    {{price|divide:'100'}}    #将数字除100
    {{price|divide:'0.01'}}   #将数字乘100
            如果需要，可以再加上floatformat:'3'这样的过滤器进行小数位的保留如
    {{price|divide:'100'|floatformat:'1'}}
    """
    try:
        if value:
            if isinstance(eval(args), (float, int)):
                return "%.2f" % (float(value) / float(args))
        else:
            return 0.00
    except Exception, e:
        return None
register.filter(divide)


def multiply(value, args):
    """
    {{price|multiply:'0.01'}}   #将数字乘100
            如果需要，可以再加上floatformat:'3'这样的过滤器进行小数位的保留如
    {{price|multiply:'100'|floatformat:'1'}}
    """
    try:
        if value:
            if isinstance(args, (float, int)) or isinstance(eval(args), (float, int)):
                return "%.2f" % (float(value) * float(args))
        else:
            return 0.00
    except Exception, e:
        return None
register.filter(multiply)


def display(value, args):
    """
            比如有这样的一个字段：foo = models.CharField(choices = (('0','新订'),('1','续订')))
            通常需要显示在页面时，在后台要做一个get_foo_display的操作才能在页面显示“新订”或者“续订”(form可以直接用select来选择)
            因此就编写了这样一个过滤器，用法如下 ：
    {{tpcustomer|display:'comment_status'}}    返回 tpcustomer.get_comment_status_display()
    """
    try:
        if value and args:
            if hasattr(value, args):
                return getattr(value, 'get_%s_display' % args)()
        else:
            return ''
    except Exception, e:
        return None
register.filter(display)

def is_recent(value, args):
    """
            判断该对象是不是最近创建，或者最近删除等
    {{k|is_recent:'create_time,5'}}    返回True或者False，天数要注意，如果是一周内，天数是6，可以是负数
    {{k|is_recent:'create_time'}}    不带天数表示是否是当天
    """
    try:
        if value and args:
            args_list = args.split(',')
            if hasattr(value, args_list[0]):
                from common.utils.utils_datetime import time_is_ndays_interval, time_is_someday
                if len(args_list) == 2:
                    return time_is_ndays_interval(getattr(value, args_list[0]), int(args_list[1]))
                elif len(args_list) == 1:
                    return time_is_someday(getattr(value, args_list[0]))
                else:
                    raise Exception()
            else:
                raise Exception()
    except Exception, e:
        return False
register.filter(is_recent)

def pic_fixer(value, args = 100):
    """
            将一些图片的地址修改成100*100、120*120等大小的
    {item.pic_url|pic_fixer}          默认是修改成100x100的
    {item.pic_url|pic_fixer:'200'}    修改成200x200的
    """
    try:
        if '_sum.jpg' in value:
            value = value.replace('_sum', '_%sx%s' % (args, args))
        else:
            value += '_%sx%s.jpg' % (args, args)
        return value
    except Exception, e:
        return value
register.filter(pic_fixer)

def display_phone(value):
    if value and value.startswith('0'):
        return '%s-%s-%s' % (value[:3], value[3:7], value[7:])
    else:
        return value
register.filter(display_phone)

def word_slice(word, arg):
    '''
    word_len截取长度
    span_class span类目
    tip_val 是否显示全部
            将长度大于20的关键词，进行简约显示。TODO：截取后导致页面上form或ajax提交word参数时，提交的word不正确，是被截取之后的。
    '''
    word_len = 18
    span_class = ''
    tip_val = 0
    if arg:
        args = arg.split(',')
        word_len = int(args[0])
        span_class = args[1]
        tip_val = int(args[2])
    try:
        if span_class:
            if len(word) > word_len and tip_val:
                return "<span class='%s' tip='%s'>%s...</span>" % (span_class, word, word[:word_len - 1])
            elif len(word) > word_len:
                return "<span class='%s'>%s...</span>" % (span_class, word[:word_len - 1])
            else:
                return "<span class='%s'>%s</span>" % (span_class, word)
        else:
            if len(word) > word_len:
                return word[:word_len - 1] + '...'
            else:
                return word
    except:
        return word
register.filter(word_slice)

def render_node_list(node_list, code = 'o', depth = 0):
    row_list = []
    row_list.append('\n' + ' ' * depth * 4 + """<ul class="indent1">""")
    node_index = 0
    for node in node_list:
        if node[1][0] == 0:
            node_index += 1
            continue
        if isinstance(node[2], list):
            sub_node_list = render_node_list(node[2][2], code + str(node_index), depth + 1)
        else:
            sub_node_list = ''
        row_list.append("""%(indent)s<li class="%(code)s%(node_index)s indent4"><label><input id="id_label_%(code)s%(node_index)s" type="checkbox" label="%(code)s%(node_index)s" onclick="or_label_check('%(code)s%(node_index)s')">%(desc)s(%(count)s个)</label> %(sub_node_list)s</li>""" % \
                        {'indent':' ' * (depth + 1) * 4,
                         'code':code,
                         'node_index':node_index,
                         'desc':node[0],
                         'count':node[1][0],
                         'sub_node_list':sub_node_list})
        node_index += 1
#    if node_index == 1:
#        return ''
    row_list.append(' ' * depth * 4 + '</ul>\n' + ' ' * depth * 4)
    return '\n'.join(row_list)

def render_or_tree(or_tree):
    return mark_safe(render_node_list([or_tree]))
register.filter(render_or_tree)

def render_node_list2(node_list, code = 'o', depth = 0, expand = 0):
    row_list = []
    node_index = 0
    for node in node_list:
        if node[1][0] == 0:
            node_index += 1
            continue
        if isinstance(node[2], list):
            sub_node_list = render_node_list2(node[2][2], code + str(node_index), depth + 1, expand)
        else:
            sub_node_list = ''

        if depth == 0:
            isexpand = 'true'
        elif depth > 2:
            isexpand = 'false'
        elif node[1][0] > 10:
            isexpand = 'true'
        else:
            isexpand = 'false'
        if expand:
            isexpand = 'true'
        if expand == '2' and '全部' in node[0]:
            showcheck = 'false'
        else:
            showcheck = 'true'
        row_list.append("""{"id":"%(code)s%(node_index)s",
                            "text":"%(desc)s(%(count)s个)",
                            "value":"%(code)s%(node_index)s",
                            "showcheck" : %(showcheck)s,
                            complete : true,
                            "isexpand" : %(isexpand)s,
                            "checkstate" : 0,
                            "hasChildren" : %(hasChildren)s
                            %(sub_node_list_text)s }""" % \
                        {'code':code,
                         'node_index':node_index,
                         'desc':node[0],
                         'count':node[1][0],
                         'isexpand':isexpand,
                         'showcheck':showcheck,
                         'hasChildren':sub_node_list and 'true' or 'false',
                         'sub_node_list_text':sub_node_list and ""","ChildNodes":%s""" % (sub_node_list)})
        node_index += 1
    return '[' + ','.join(row_list) + ']'

def render_or_tree2(or_tree, expand):
    return mark_safe(render_node_list2([or_tree], 'o', 0, expand))
register.filter(render_or_tree2)

@register.filter
def truncatechars(value, arg):
    try:
        arg = int(arg)
        return value[:max(arg, 0)]
    except:
        return value

@register.filter
def truncatechars_ch(value, arg):
    '''根据字符长度截断字符串，汉字计算为两个字符'''
    try:
        arg = int(arg)
    except:
        return value
    if arg > 0:
        word = ''
        word_length = 0
        for char in value:
            if char >= u'\u4e00' and char <= u'\u9fa5':
                word_length += 2
            else:
                word_length += 1
            if word_length <= arg:
                word += char
            else:
                word += '...'
                break
        return word
    else:
        return value

@register.filter
def file_time_stamp(value):
    """在 js/css 后面添加最后修改时间的时间戳，如： /js/c.js -> /js/c.js?fmts=1289377595.3如果没找取对应的文件，则直接返回原value"""
    ROOT_PATH = settings.PROJECT_ROOT

    if value.startswith("/"):
        fn = os.path.join(ROOT_PATH, value[1:].replace("/", os.sep))

    if os.path.isfile(fn):
        ts = os.stat(fn).st_mtime
        sp = "?" if "?" not in value else "&"
        value = "%s%sv=%.1f" % (value, sp, ts)
    return value


@register.filter
def static_url(value):
    """在 js/css/img 前面加上 STATIC_URL, 后面添加最后修改时间的时间戳"""
    ts = time.time()
    if not settings.DEBUG:
        static_path = os.path.join(settings.STATIC_ROOT, value.replace("/", os.sep))
        if os.path.isfile(static_path):
            ts = os.stat(static_path).st_mtime
    sp = "?" if "?" not in value else "&"
    return settings.STATIC_URL + value + sp + 'v=%.1f' % ts


@register.filter
def media_url(value):
    """在 js/css/img 前面加上 MEDIA_URL, 后面添加最后修改时间的时间戳"""
    ts = time.time()
    if not settings.DEBUG:
        media_path = os.path.join(settings.MEDIA_ROOT, value.replace("/", os.sep))
        if os.path.isfile(media_path):
            ts = os.stat(media_path).st_mtime
    sp = "?" if "?" not in value else "&"
    return settings.MEDIA_URL + value + sp + 'v=%.1f' % ts


@register.filter
def get_attr(value, args):
    """应用于动态取属性的值{{adgroup|get_attr:'campaign_id'}}"""
    result = getattr(value, args, None) or ''
    if callable(result):
        result = result()
    return result

@register.filter
def trim(value):
    return value.strip()

@register.filter
def txrange(value, args):
    """生成指定长度的迭代对象，便于前台循环  6|txrange:0 表示生成0到6的迭代对象"""
    return xrange(args, int(value))

@register.filter
def range_reverse(value, args):
    """生成指定长度的迭代对象，便于前台循环  6|txrange_desc:1 表示生成6到1的迭代对象"""
    return xrange(int(value), args, -1)

@register.filter
def get_list(value, args):
    """获取list的值"""
    return (len(value) - 1) >= args and value[args] or None

@register.filter
def get_dict(value, args):
    """获取object,dict的值"""
    if isinstance(value, object) and hasattr(value, args):
        return get_attr(value, args)

    if isinstance(value, dict):
        return value.get(args, None)

    return None


# 前台url添加active
@register.simple_tag(takes_context=True)
def active_url(context, url_name, active_class='active'):
    active_url_name = context['request'].resolver_match.url_name
    if active_url_name == url_name or active_url_name in NAV_URL_DICT.get(url_name, []):
        return active_class
    else:
        return ''


# 变量布尔值展示
@register.simple_tag()
def bool_str(bool, true='是', false='否'):
    if bool:
        return true
    else:
        return false


@register.tag(name='checkPerm')
def do_check_permission(parser, token):
    try:
        tag_name, per_name = token.split_contents()
    except:
        raise TemplateSyntaxError(" tag  error!")
    nodelist = parser.parse('endcheckPerm')
    parser.delete_first_token()
    return CheckPermission(nodelist, per_name)


class CheckPermission(Node):
    """验证是否有权限"""
    per_name = ''

    def __init__(self, nodelist, per_name):
        self.nodelist = nodelist
        self.per_name = per_name

    def render(self, context):
        user = context.request.user
        if user.has_perm(self.per_name):
            output = self.nodelist.render(context)
        else:
            output = ''
        return output


@register.tag(name='notHasPerm')
def do_check_permission(parser, token):
    """验证是否有权限，自定义标签"""
    try:
        tag_name, per_name = token.split_contents()
    except:
        raise TemplateSyntaxError(" tag  error!")
    nodelist = parser.parse('endnotHasPerm')
    parser.delete_first_token()
    return CheckHasPermission(nodelist, per_name)


class CheckHasPermission(Node):
    """验证是否有权限"""
    per_name = ''

    def __init__(self, nodelist, per_name):
        self.nodelist = nodelist
        self.per_name = per_name

    def render(self, context):
        user = context.request.user
        if user.has_perm(self.per_name):
            output = ''
        else:
            output = self.nodelist.render(context)
        return output
