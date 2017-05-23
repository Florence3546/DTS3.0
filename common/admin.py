from django.contrib import admin

from .models import GlobalConfig
from .models import Region


class GlobalConfigAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_cn', 'value', 'note', 'parent')

admin.site.register(GlobalConfig, GlobalConfigAdmin)


class RegionAdmin(admin.ModelAdmin):
    list_display = ('region_code', 'region_name', 'parent_id', 'region_level', 'region_order', 'region_name_en', 'region_shortname_en')
    list_editable = ['region_order']
    list_display_links = ('region_name',)

admin.site.register(Region, RegionAdmin)
