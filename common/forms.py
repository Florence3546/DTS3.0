# coding=UTF-8
from __future__ import unicode_literals

from django.forms import ModelForm
from .models import SettingsType, SettingsItem
from .models import Region


class SettingsTypeForm(ModelForm):
    class Meta:
        model = SettingsType
        fields = ['code', 'name', 'note']


class SettingsItemForm(ModelForm):
    class Meta:
        model = SettingsItem
        fields = ['name', 'value', 'note', 's_type']


class RegionForm(ModelForm):
    class Meta:
        model = Region
        fields = ['region_code', 'region_name', 'parent_id', 'region_level', 'region_order', 'region_name_en', 'region_shortname_en']




