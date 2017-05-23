# coding=UTF-8
from __future__ import unicode_literals
from django import forms
from django.forms import ModelForm
from ckeditor_uploader.fields import RichTextUploadingFormField

from .models import Good, DrugAttr, GoodCategory, LackRegister


class GoodForm(ModelForm):
    class Meta:
        model = Good
        fields = '__all__'


class DrugAttrForm(ModelForm):
    class Meta:
        model = DrugAttr
        fields = '__all__'


class GoodCategoryForm(ModelForm):
    class Meta:
        model = GoodCategory
        fields = ['name', 'path']


class GoodDrugAttrForm(forms.Form):
    """商品列表添加Form"""
    fk_good_id = forms.IntegerField(required=False)
    external_id = forms.CharField(required=True, max_length=80)
    name = forms.CharField(required=True, max_length=80)
    trade_name = forms.CharField(required=True, max_length=80)
    brand = forms.CharField(required=False, max_length=30)
    category = forms.IntegerField(required=True)
    supplier = forms.IntegerField(required=False)
    manufacturer = forms.CharField(required=True)
    locality = forms.CharField(required=True, max_length=20)  # 如：浙江 杭州，湖北 武汉，北京，上海
    # 包装价格
    unit = forms.CharField(required=True, max_length=10)  # 如：盒，瓶，箱，袋
    prep_spec = forms.CharField(required=True, max_length=30)  # 如：0.5g
    pack_spec = forms.CharField(required=True, max_length=10)  # 如：瓶100片，可用药品电子监管码查询到
    retail_price = forms.IntegerField(required=True)  # 单位：分
    member_price = forms.IntegerField(required=True)  # 单位：分
    # 库存数量定期从中间数据库中的 GoodStock 去读取，并更新本地数据库
    stock_amount = forms.IntegerField(required=True)
    # 商品属性
    license = forms.CharField(required=True)
    dosage_form = forms.CharField(required=False)
    otc_type = forms.IntegerField(required=False)
    recipe_type = forms.CharField(required=False)
    is_otc = forms.IntegerField(required=True)
    is_zybh = forms.IntegerField(required=True)
    is_new = forms.IntegerField(required=True)  # 新药：未曾在中国境内上市销售的药品。
    is_oem = forms.IntegerField(required=True)
    desc_drug = RichTextUploadingFormField(required=False)
    desc_good = RichTextUploadingFormField(required=False)


class LackRegisterForm(ModelForm):
    class Meta:
        model = LackRegister
        fields = '__all__'
