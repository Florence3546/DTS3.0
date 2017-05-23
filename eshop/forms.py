# coding=UTF-8
from __future__ import unicode_literals

from django import forms
from .models import TestUploadFile
from dtsauth.models import User

from dtsadmin.models import ConsultFeedback

# 验证码
from captcha.fields import CaptchaField


class TestUploadFileForm(forms.ModelForm):
    class Meta:
        model = TestUploadFile
        fields = ['photo']


class LoginForm(forms.Form):
    """用户登录"""
    name = forms.CharField(required=True, max_length=150,
                           error_messages={"required": "用户名不能为空", "max_length": "用户名最大长度150"})
    passwd = forms.CharField(required=True, max_length=128,
                             error_messages={"required": "密码不能为空", "max_length": "用户名最大长度128"})
    captcha = CaptchaField(required=True, error_messages={"required": "验证码不能为空"})

    # name = forms.CharField(required=True, max_length=150)
    # passwd = forms.CharField(required=True, max_length=128)
    # captcha = CaptchaField(required=True)


class LoginPhoneForm(forms.Form):
    """电话登录"""
    phone = forms.CharField(required=True, max_length=12,error_messages={"required": "电话不能为空"})  # 电话号码 11位
    # captcha = CaptchaField()                                    # 验证码


class ForgetPasswordForm(forms.Form):
    """用户登录"""
    # name = forms.CharField(required=True, max_length=150)  # 字符串类型，必填字段，最大长度150
    phone = forms.CharField(required=True, max_length=12)  # 电话号码 11位
    captcha = CaptchaField()  # 验证码


class AccountSafetyForm(forms.Form):
    """账户安全"""
    # name = forms.CharField(required=True, max_length=150)  # 字符串类型，必填字段，最大长度150
    phone = forms.CharField(required=True, max_length=12)  # 电话号码 11位
    captcha = CaptchaField()  # 验证码


class RegisterForm(forms.Form):
    """用户注册"""
    username = forms.CharField(required=True, min_length=3, max_length=16,
                               error_messages={"required": "用户名不能为空", "min_length": "用户名太短至少3位",
                                               "max_length": "用户名太长最多16位"})
    first_name = forms.CharField(required=True, error_messages={"required": "用户姓名必填"})
    phone = forms.CharField(required=True, min_length=8, max_length=11,
                            error_messages={"required": "电话必填", "min_length": "这不是一个正确的手机号码"})
    passwd = forms.CharField(required=True, min_length=5,
                             error_messages={"required": "密码不能为空", "min_length": "密码太短至少5位"})
    passwd2 = forms.CharField(required=True, min_length=5,
                              error_messages={"required": "重复密码不能为空", "min_length": "密码太短至少5位"})
    gender = forms.IntegerField(required=True)
    email = forms.EmailField(required=True)
    # todo Validates email


class MerchantRegisterForm(RegisterForm):
    """企业用户注册"""
    enterprise_name = forms.CharField(required=True, min_length=2,
                                      error_messages={"required": "单位全称必填", "min_length": "单位全称最少2位"})
    short_name = forms.CharField(required=True, min_length=2,
                                 error_messages={"required": "单位简称必填", "min_length": "单位简称最少2位"})
    operate_mode = forms.CharField(required=True, error_messages={"required": "所在地区必填"})
    region = forms.CharField(required=True, error_messages={"required": "所在地区必填"})
    address = forms.CharField(required=True, error_messages={"required": "单位地址必填"})
    enter_phone = forms.CharField(required=True, min_length=6, error_messages={"min_length": "电话最少6位"})
    legal_repr = forms.CharField(required=True, max_length=30,
                                 error_messages={"required": "法定代表人必填", "max_length": "最多30位"})
    biz_scope = forms.CharField(required=True, error_messages={"required": "经营范围必填"})
    qyxk = forms.FileField(required=True, error_messages={"required": "请上传企业资质文件以便快速审核通过"})  # 企业许可证
    yyzz = forms.FileField(required=False)  # 营业执照
    wts = forms.FileField(required=False)  # 法人委托书


class AccountInfoForm(forms.ModelForm):
    """账户信息"""

    # first_name = forms.CharField(required=True, min_length=3)
    # phone = forms.CharField(required=True, min_length=8, max_length=11)
    # gender = forms.IntegerField(required=True)
    # email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'phone', 'gender', 'email']


class ConsultFeedbackForm(forms.ModelForm):
    """咨询反馈"""

    class Meta:
        model = ConsultFeedback
        fields = ['user', 'content', 'feedback_type']


# 验证码
class CaptchaTestForm(forms.Form):
    # name = forms.CharField()
    captcha = CaptchaField()
