from django.contrib import admin

# Register your models here.
from .models import Good, GoodCategory, DrugAttr, DosageForm, GoodQualification, GoodPhoto, LackRegister

class GoodAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_id', 'name', 'trade_name', 'brand', 'category', 'supplier', 'manufacturer', 'locality', 'pinyin', 'pinyin_tn',   'unit', 'prep_spec', 'pack_spec', 'barcode', 'retail_price', 'member_price', 'stock_amount', 'main_photo', 'is_online', 'is_qualified')

admin.site.register(Good, GoodAdmin)


class GoodCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'path')

admin.site.register(GoodCategory, GoodCategoryAdmin)


class DrugAttrAdmin(admin.ModelAdmin):
    list_display = ('good', 'license', 'valid_from', 'valid_to', 'quality_standard', 'dosage_form', 'is_auth', 'is_otc', 'is_zybh', 'is_new', 'is_oem', 'otc_type', 'recipe_type', 'suitable_crowd', 'desc_drug', 'desc_good', 'storage_condition')

admin.site.register(DrugAttr, DrugAttrAdmin)


class DosageFormAdmin(admin.ModelAdmin):
    list_display = ()

admin.site.register(DosageForm, DosageFormAdmin)


class GoodQualificationAdmin(admin.ModelAdmin):
    list_display = ()

admin.site.register(GoodQualification, GoodQualificationAdmin)


class GoodPhotoAdmin(admin.ModelAdmin):
    list_display = ('good', 'photo', 'order_no', 'upload_man', 'upload_time')

admin.site.register(GoodPhoto, GoodPhotoAdmin)


class LackRegisterAdmin(admin.ModelAdmin):
    list_display = ('people', 'good', 'created', 'note')

admin.site.register(LackRegister, LackRegisterAdmin)
