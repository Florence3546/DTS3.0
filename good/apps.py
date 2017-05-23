# coding=UTF-8
from __future__ import unicode_literals

from django.apps import AppConfig


class GoodConfig(AppConfig):
    name = 'good'
    verbose_name = u'产品及产品资质管理'

    reserved_dosage_form = [
        ('片剂', 'PJ'),
        ('胶囊剂', 'JNJ'),
        ('颗粒剂', 'KLJ'),
        ('乳剂', 'RJ'),
        ('溶液剂', 'RYJ'),
        ('混悬剂', 'HXJ'),
        ('注射剂', 'ZSJ'),
        ('喷雾剂', 'PWJ'),
        ('气雾剂', 'QWJ'),
        ('粉雾剂', 'FWJ'),
        ('外用溶液剂', 'WYRYJ'),
        ('洗剂', 'XJ'),
        ('搽剂', 'CJ'),
        ('软膏剂', 'RGJ'),
        ('硬膏剂', 'YGJ'),
        ('糊剂', 'HJ'),
        ('贴剂', 'TJ'),
        ('滴眼剂', 'DYJ'),
        ('滴鼻剂', 'DBJ'),
        ('眼用软膏剂', 'YYRGJ'),
        ('合漱剂', 'HSJ'),
        ('舌下片剂', 'SXPJ'),
        ('粘贴片', 'ZTJ'),
        ('贴膜剂', 'TMJ'),
        ('栓剂', 'SJ'),
        ('泡腾片', 'PTP'),
        ('滴剂', 'DJ'),
        ('滴丸剂', 'DWJ'),
    ]

    reserved_efficacy_class = [
        {'name': '抗生素类', 'pinyin': 'KSSL', 'children': [
            {'name': '抗生素类', 'pinyin': 'KSSL', 'children': []},
        ]},
    ]
