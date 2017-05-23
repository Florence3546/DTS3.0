# coding=UTF-8
from __future__ import unicode_literals

from django.db import models
from common.constant import PAGE_CHOICES
from good.models import Good
from dtsauth.models import User
from order.models import Order
import datetime
from common.constant import SITE_MESSAGE_TYPE


def test_file_path(obj, filename):
    return u'测试图片/%(date)s/%(filename)s' % {
        'date': datetime.date.today(),
        'filename': filename,
    }


class TestUploadFile(models.Model):
    photo = models.ImageField('图片', upload_to=test_file_path)


def page_section_path(obj, filename):
    section = obj.section
    return '页面区域/%(page)s/%(section)s/%(filename)s' % {
        'page': section.get_page_display(),
        'section': '%s #%s' % (section.title, section.anchor),
        'filename': filename,
    }


class PageSection(models.Model):
    """页面区域"""
    title = models.CharField('标题', max_length=30)
    page = models.CharField('所属页面', max_length=30, choices=PAGE_CHOICES)
    anchor = models.CharField('锚点', max_length=30, blank=True)
    icon = models.CharField('icon代码', max_length=50, blank=True)
    href = models.CharField('超链接', max_length=100, blank=True)
    order_no = models.IntegerField('显示排序', blank=True, null=True)
    is_display = models.BooleanField('是否显示', default=True)
    parent = models.ForeignKey('self', verbose_name='父级', blank=True, null=True, on_delete=models.PROTECT,
                               related_name='children')

    def __unicode__(self):
        return '<%s> %s #%s' % (self.get_page_display(), self.title, self.anchor)

    @classmethod
    def build_tree_by_page(cls, page):
        """获取某个页面的区域树"""

        def set_child_list(self, data_dict):
            self.child_list = data_dict.get(self.id, [])
            for child in self.child_list:
                set_child_list(child, data_dict)

        section_set = cls.objects.select_related('parent').filter(page=page, is_display=True).order_by('parent',
                                                                                                       'order_no')
        image_set = SectionImage.objects.filter(section__in=section_set).order_by('order_no')
        href_set = SectionHref.objects.filter(section__in=section_set).order_by('order_no')
        good_set = SectionGood.objects.filter(section__in=section_set).order_by('order_no')

        image_dict = {}
        for image in image_set:
            image_dict.setdefault(image.section.id, []).append(image)
        href_dict = {}
        for href in href_set:
            href_dict.setdefault(href.section.id, []).append(href)
        good_dict = {}
        for good in good_set:
            good_dict.setdefault(good.section.id, []).append(good)

        parent_dict = {}
        for obj in section_set:
            obj.sectionimage_list = image_dict.get(obj.id, [])
            obj.sectionhref_list = href_dict.get(obj.id, [])
            obj.sectiongood_list = good_dict.get(obj.id, [])
            temp_key = obj.parent.id if obj.parent else ''
            parent_dict.setdefault(temp_key, []).append(obj)
        root_list = parent_dict.get('', [])
        for obj in root_list:
            set_child_list(obj, parent_dict)
        return {root.anchor: root for root in root_list}


class SectionImage(models.Model):
    """页面区域图片及跳转链接"""
    section = models.ForeignKey(PageSection, verbose_name='页面区域')
    image = models.ImageField('图片', upload_to=page_section_path)
    href = models.CharField('超链接', max_length=100, blank=True)
    alt = models.CharField('替代文本', max_length=10, blank=True)
    order_no = models.IntegerField('显示排序', blank=True, null=True)


class SectionHref(models.Model):
    """页面区域文本超链接"""
    section = models.ForeignKey(PageSection, verbose_name='页面区域')
    text = models.CharField('文本', max_length=30)
    href = models.CharField('超链接', max_length=100, blank=True)
    order_no = models.IntegerField('显示排序', blank=True, null=True)


class SectionGood(models.Model):
    """页面区域产品"""
    section = models.ForeignKey(PageSection, verbose_name='页面区域')
    good = models.ForeignKey(Good, verbose_name='产品')
    is_lock = models.BooleanField('锁定', default=False)
    order_no = models.IntegerField('显示排序', blank=True, null=True)


class SiteMessage(models.Model):
    user = models.ForeignKey(User, verbose_name="用户")
    order = models.ForeignKey(Order, verbose_name="订单", blank=True, null=True)
    msg_type = models.IntegerField("消息类型", choices=SITE_MESSAGE_TYPE)
    contant = models.TextField("类容")
    is_read = models.BooleanField("是否已读")
    time = models.DateTimeField("时间", auto_now_add=True)
