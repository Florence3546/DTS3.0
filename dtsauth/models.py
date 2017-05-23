# coding=UTF-8
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

from common.constant import USERTYPE_CHOICES, REVIEW_STATUS_CHOICES, REVIEWING, GENDER_CHOICE, RECORD_DATA_TYPE_CHOICES
from common.models import SettingsType
from bpmn.models import Process
import datetime


class Permission(models.Model):
    """自定义权限"""
    codename = models.CharField('权限码', max_length=80, unique=True)
    name = models.CharField('权限名', max_length=50)
    note = models.TextField('备注', blank=True)
    is_active = models.BooleanField('权限状态', default=False)
    parent = models.ForeignKey('Permission', verbose_name='父级节点', blank=True, null=True)

    def __unicode__(self):
        return self.name


# todo 会员积分 会员等级 字段
# 会员等级
class MenberLevel(models.Model):
    """会员等级"""
    pass


class Enterprise(models.Model):
    """企业/单位"""
    external_id = models.CharField('外部系统企业ID', max_length=30, blank=True, null=True, unique=True)  # 如：从时空导入的企业数据
    name = models.CharField('单位全称', max_length=80)  # 如：天津力生制药股份有限公司
    short_name = models.CharField('单位简称', max_length=20, default='')  # 如：力生制药
    pinyin = models.CharField('拼音码', max_length=20, default='')  # 如：LSZY
    biz_scope = models.CharField('经营范围', max_length=500, blank=True)
    economic_type = models.CharField('企业经济类型', max_length=30, blank=True)  # 如：股份制
    region = models.CharField('所在地区', blank=True, max_length=50)  # 省市区 三级
    address = models.TextField('单位地址', blank=True)  # 详细地址
    city = models.CharField('城市', max_length=20, blank=True)
    note = models.TextField('备注', blank=True)
    review_status = models.IntegerField('审核状态', default=REVIEWING, choices=REVIEW_STATUS_CHOICES, blank=True)
    is_master = models.BooleanField('是否货主', default=False)
    is_lock = models.BooleanField('是否锁定', default=False)
    subbranch = models.CharField('开户支行', max_length=50, blank=True)
    bank_account = models.CharField('银行账号', max_length=50, blank=True)
    reg_capital = models.CharField('注册资本', max_length=30, blank=True)
    operate_mode = models.CharField('经营方式', max_length=30, blank=True)  # 批发 零售 医院 诊所 终端 医疗机构 非营利性医疗机构
    reg_no = models.CharField('机构登记证号', max_length=30, blank=True)
    org_code = models.CharField('统一社会信用代码/组织机构代码', max_length=30, blank=True)
    legal_repr = models.CharField('法定代表人', max_length=30, blank=True)
    reg_authority = models.CharField('登记机关', max_length=50, blank=True)
    valid_from = models.DateField('营业期限自', blank=True, null=True)
    valid_to = models.DateField('营业期限至', blank=True, null=True)
    contact = models.CharField('联系人', max_length=30, blank=True)
    phone = models.CharField('联系电话', max_length=30, blank=True)
    website = models.CharField('官网', max_length=50, blank=True)
    email = models.EmailField('邮箱', blank=True)
    fax = models.CharField('传真', max_length=30, blank=True)
    created = models.DateTimeField('创建时间', default=datetime.datetime.now)

    # 交易相关字段
    balance = models.IntegerField('商城余额', default=0, blank=True, null=True)  # 单位：分
    overdraft = models.IntegerField('透支额度', default=0, blank=True, null=True)  # 单位：分
    overdrew = models.DateTimeField('透支时间', blank=True, null=True)

    def __unicode__(self):
        return self.name


class Role(models.Model):
    """角色"""
    name = models.CharField('角色名称', max_length=50)
    usertype = models.CharField('用户类型', max_length=20, choices=USERTYPE_CHOICES)
    desc = models.TextField('角色描述', max_length=200, blank=True)
    is_reserved = models.BooleanField('不可删改', default=False)

    class Meta:
        unique_together = (('usertype', 'name'),)

    def __unicode__(self):
        return self.name


class DtsUserManager(UserManager):
    def get_queryset(self):
        return super(DtsUserManager, self).get_queryset().select_related('enterprise').prefetch_related('role')


class User(AbstractUser):
    """
    自定义用户，已继承字段：
    username,      // CharField
    password,      // CharField
    first_name,    // CharField  用户姓名中文
    last_name,     // CharField
    email,         // EmailField
    is_staff,      // BooleanField
    is_active,     // BooleanField  用户状态 激活(未锁定) 未激活(已锁定) 
    is_superuser,  // BooleanField
    date_joined,   // DateTimeField
    last_login,    // DateTimeField
    """
    usertype = models.CharField('用户类型', max_length=20, choices=USERTYPE_CHOICES, default='Members')
    gender = models.IntegerField('性别', choices=GENDER_CHOICE, blank=True, null=True)
    phone = models.CharField('联系电话', max_length=20, blank=True)
    enterprise = models.ForeignKey(Enterprise, verbose_name='企业/单位', blank=True, null=True, on_delete=models.PROTECT)
    role = models.ManyToManyField(Role, verbose_name='角色', blank=True)
    balance = models.IntegerField('账户余额', default=0, blank=True, null=True)  # 单位：分
    pay_password = models.CharField('支付密码', max_length=128, blank=True, null=True)
    is_master = models.BooleanField('是否企业主账号', default=False, blank=True)
    is_accorded = models.BooleanField('是否同意购销协议', default=False, blank=True)
    is_forbidden = models.BooleanField('是否禁用', default=False, blank=True)
    is_deleted = models.BooleanField('是否删除', default=False, blank=True)
    note = models.TextField('备注', blank=True)
    proc_register = models.OneToOneField(Process, verbose_name='注册流程', blank=True, null=True)
    department = models.CharField('部门', max_length=50, blank=True)
    objects = DtsUserManager()

    def get_dts_user_permissions(self):
        if not hasattr(self, '_dts_user_perm_cache'):
            self._dts_user_perm_cache = set(UserPermission.objects.filter(user=self).values_list('codename', flat=True))
        return self._dts_user_perm_cache

    def get_dts_role_permissions(self):
        if not hasattr(self, '_dts_role_perm_cache'):
            self._dts_role_perm_cache = set(RolePermission.objects.filter(role__in=self.role.all()).values_list('codename', flat=True))
        return self._dts_role_perm_cache

    def get_all_dts_permissions(self):
        if not hasattr(self, '_dts_perm_cache'):
            self._dts_perm_cache = self.get_dts_user_permissions()
            self._dts_perm_cache.update(self.get_dts_role_permissions())
        return self._dts_perm_cache

    def has_perm(self, perm, obj=None):
        if not super(User, self).has_perm(perm, obj):
            return perm in self.get_all_dts_permissions()
        return True

    def clear_perm_cache(self):
        delattr(self, '_dts_perm_cache')
        delattr(self, '_dts_user_perm_cache')
        delattr(self, '_dts_role_perm_cache')

    @staticmethod
    def get_usertype_choices():
        return SettingsType.get_item_choices('USERTYPE')


class RolePermission(models.Model):
    """角色权限关联表"""
    role = models.ForeignKey(Role, verbose_name='角色', on_delete=models.CASCADE)
    codename = models.CharField('权限码', max_length=80)


class UserPermission(models.Model):
    """用户权限关联表"""
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    codename = models.CharField('权限码', max_length=80)


def enterprise_qualification_path(obj, filename):
    enter = obj.enterprise
    return '企业资质/%(index)s/%(enter_name)s/%(filename)s' % {
        'index': enter.pinyin[0].upper(),
        'enter_name': enter.name,
        'filename': filename,
    }


class EnterpriseQualification(models.Model):
    """企业资质文件"""
    enterprise = models.ForeignKey(Enterprise, verbose_name='企业', on_delete=models.CASCADE)
    photo = models.ImageField('图片', upload_to=enterprise_qualification_path)
    upload_man = models.ForeignKey(User, verbose_name='上传人', on_delete=models.CASCADE, blank=True, null=True)
    # photo_name = models.CharField('图片描述', max_length=80)
    upload_time = models.DateTimeField('上传时间', auto_now_add=True)


class BusinessScope(models.Model):
    """经营范围"""
    name = models.CharField('名称', max_length=50)


class OperateRecord(models.Model):
    """操作记录"""
    operate = models.CharField('操作名', max_length=30)
    operate_cn = models.CharField('中文', max_length=30)
    process = models.ForeignKey(Process, verbose_name='处理流程', blank=True, null=True)
    operator = models.ForeignKey(User, verbose_name='操作人', blank=True, default=None)
    note = models.TextField('备注', blank=True)
    created = models.DateTimeField('创建时间', auto_now_add=True)
    data_type = models.CharField('数据类型', max_length=20, choices=RECORD_DATA_TYPE_CHOICES)
    data_id = models.IntegerField('数据ID', blank=True, null=True)

