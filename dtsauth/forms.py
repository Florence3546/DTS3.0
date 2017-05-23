# coding=UTF-8
from __future__ import unicode_literals

from django.forms import ModelForm
from django import forms
from .models import Enterprise, User,Role, Permission


class RoleForm(ModelForm):
    class Meta:
        model = Role
        fields = ['name', 'usertype', 'desc']


class PermissionForm(ModelForm):
    class Meta:
        model = Permission
        fields = ['codename', 'name', 'note', 'is_active']


class EnterpriseForm(ModelForm):
    class Meta:
        model = Enterprise
        # fields = '__all__'
        fields = ['external_id',
                  'name',
                  'short_name',
                  # 'pinyin',
                  'biz_scope',
                  'economic_type',
                  'address',
                  'city',
                  'note',
                  'is_master',
                  'is_lock',
                  # 'review_status'
                  # 'is_qualified',
                  # 'is_active',
                  'subbranch',
                  'bank_account',
                  'reg_capital',
                  'operate_mode',
                  'reg_no',
                  'org_code',
                  'legal_repr',
                  'reg_authority',
                  'valid_from',
                  'valid_to',
                  'contact',
                  'phone',
                  'website',
                  'email',
                  'fax',
                  'region',
                  'balance',
                  'overdraft',
                  'overdrew', ]


class UserForm(ModelForm):
    class Meta:
        model = User
        # fields = '__all__'
        fields = ['username', 'first_name', 'email', 'phone', 'gender', 'password', 'enterprise', 'role', 'department', 'is_master']


class RoleAttrForm(forms.Form):
    name = forms.CharField(required=True)
    usertype = forms.CharField(required=True)
    desc = forms.CharField(required=False)

    class Meta:
        unique_together = (('usertype', 'name'),)

