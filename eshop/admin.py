from django.contrib import admin

from eshop.models import (
    PageSection,
    SectionImage,
    SectionHref,
    SectionGood,
    SiteMessage,
)


@admin.register(SiteMessage)
class SiteMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'msg_type', 'contant', 'is_read')


@admin.register(PageSection)
class PageSectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'parent', 'page', 'anchor', 'href', 'order_no', 'is_display')
    list_filter = ('parent',)


@admin.register(SectionImage)
class SectionImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'section', 'href', 'alt', 'order_no')
    list_filter = ('section',)


@admin.register(SectionHref)
class SectionHrefAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'section', 'href', 'order_no')
    list_filter = ('section',)


@admin.register(SectionGood)
class SectionGoodAdmin(admin.ModelAdmin):
    list_display = ('id', 'good', 'section', 'is_lock', 'order_no')
    list_filter = ('section',)
    raw_id_fields = ('good',)
