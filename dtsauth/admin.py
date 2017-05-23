from django.contrib import admin

from dtsauth.models import (Permission,
                            Enterprise,
                            Role,
                            RolePermission,
                            User,
                            UserPermission,
                            OperateRecord,
                            EnterpriseQualification)


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'email', 'usertype', 'phone', 'enterprise', 'is_master', 'is_staff',
                    'is_active', 'is_superuser', 'is_deleted', 'date_joined', 'last_login', 'note')



class EnterpriseAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'external_id', 'address', 'city')


class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'usertype', 'is_reserved', 'desc')


class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ('role', 'codename')


class UserPermissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'codename')


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Enterprise, EnterpriseAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(RolePermission, RolePermissionAdmin)
admin.site.register(UserPermission, UserPermissionAdmin)


class PermissionAdmin(admin.ModelAdmin):
    list_display = ('codename', 'name', 'note', 'is_active', 'parent')


admin.site.register(Permission, PermissionAdmin)


class EnterpriseQualificationAdmin(admin.ModelAdmin):
    list_display = ('enterprise', 'photo', 'upload_man', 'upload_time')


admin.site.register(EnterpriseQualification, EnterpriseQualificationAdmin)

class OperateRecordAdmin(admin.ModelAdmin):
    list_display = ('operate', 'operate_cn', 'process', 'operator', 'note', 'data_type', 'data_id')


admin.site.register(OperateRecord, OperateRecordAdmin)

