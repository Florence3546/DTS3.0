# coding=UTF-8
from __future__ import unicode_literals

from django.db import models

from common.constant import OTC_TYPE_CHOICES, REVIEW_STATUS_CHOICES, ONLINE_CHOICES, STOCK_STATUS_CHOICES, OUT_OF_STOCK
from dtsauth.models import Enterprise, User
from promotion.models import GoodPromotion, PurchaseAgreement

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class Good(models.Model):
    """产品基本信息"""
    external_id = models.CharField('外部系统编码', max_length=80, blank=True)  # 如：时空系统ksoa 的 GOODSID
    name = models.CharField('通用名', max_length=80)  # 如：对乙酰氨基酚
    trade_name = models.CharField('商品名', max_length=80)  # 如：百服咛
    brand = models.CharField('品牌', max_length=30, blank=True, null=True, default='')  # 如：感康
    category = models.ForeignKey('GoodCategory', verbose_name='商品分类', on_delete=models.PROTECT, related_name='category', blank=True, null=True)
    external_category = models.CharField(verbose_name='商品分类', max_length=30, blank=True)  # 值为企业经营范围中的一部分
    extra_category = models.CharField(verbose_name='商品其他分类', max_length=30, blank=True)
    supplier = models.ForeignKey(Enterprise, verbose_name='供应商', on_delete=models.PROTECT, related_name='supp_goods', blank=True, null=True)
    manufacturer = models.CharField('厂家', max_length=200, blank=True, null=True)
    locality = models.CharField('产地', max_length=20)  # 如：浙江 杭州，湖北 武汉，北京，上海
    pinyin = models.CharField('通用名拼音码', max_length=20)
    pinyin_tn = models.CharField('商品名拼音码', max_length=20)

    # 包装价格
    unit = models.CharField('包装单位', max_length=10, blank=True)  # 如：盒，瓶，箱，袋
    prep_spec = models.CharField('制剂规格', max_length=30, blank=True)  # 如：0.5g
    pack_spec = models.CharField('包装规格', max_length=10, blank=True)  # 如：瓶100片，可用药品电子监管码查询到
    external_spec = models.CharField('外部系统规格', max_length=50, blank=True)  # 如：时空系统ksoa 的 0.5g*7片
    barcode = models.CharField('商品条码', max_length=20, blank=True)
    retail_price = models.IntegerField('零售价', blank=True, null=True)  # 单位：分
    member_price = models.IntegerField('会员价', blank=True, null=True)  # 单位：分

    # 库存数量定期从中间数据库中的 GoodStock 去读取，并更新本地数据库
    stock_amount = models.IntegerField('库存数量', blank=True, null=True)
    main_photo = models.ImageField('商品主图', upload_to='good/%Y/%m/%d/', blank=True)
    online_time = models.DateTimeField('最新上架时间', blank=True, null=True)
    promotion = models.ForeignKey(GoodPromotion, verbose_name='当前促销活动', blank=True, null=True)
    is_online = models.IntegerField('是否上架', blank=True, null=True, choices=ONLINE_CHOICES, default=0)
    is_qualified = models.IntegerField('审核状态', choices=REVIEW_STATUS_CHOICES, default=1, blank=True, null=True)

    def __unicode__(self):
        return self.name

    def get_display_name(self):
        return self.brand + ' ' + self.name + ' ' + self.trade_name

    @property
    def display_spec(self):
        return self.external_spec or '%s %s' % (self.prep_spec, self.pack_spec)


class GoodCategory(models.Model):
    """产品分类"""
    name = models.CharField('分类名', max_length=30)  # 如：抗生素类
    path = models.CharField('分类路径', max_length=50, default='/', blank=True)  # 如：id为6的分类其路径为/1/2/4/, 路径中不包括自身id

    def __unicode__(self):
        return self.name

    @classmethod
    def get_path_display(cls, path):
        id_list = [int(_id) for _id in path.split('/') if _id]
        if id_list:
            qs = cls.objects.filter(id__in=id_list).only('id', 'name')
            name_dict = {obj.id: obj.name for obj in qs}
            name_list = [name_dict.get(_id, str(_id)) for _id in id_list]
            return '/%s/' % ('/'.join(name_list))
        else:
            return '/'

    @property
    def path_display(self):
        if not hasattr(self, '_path_display'):
            self._path_display = self.get_path_display(self.path)
        return self._path_display

    @property
    def full_path(self):
        return '%s%s/' % (self.path, self.id)

    @property
    def full_path_display(self):
        if not hasattr(self, '_full_path_display'):
            self._full_path_display = self.get_path_display(self.full_path)
        return self._full_path_display


class DrugAttr(models.Model):
    """药品特性"""
    good = models.OneToOneField(Good, verbose_name='产品', blank=True, null=True)
    external_id = models.CharField('外部系统编码', max_length=80, blank=True)  # 如：时空系统ksoa 的 GOODSID
    license = models.CharField('批准文号', max_length=80)  # 如：'国药准字Z' 代表中成药
    valid_from = models.DateField('批准文号生效日期', blank=True, null=True)
    valid_to = models.DateField('批准文号失效日期', blank=True, null=True)
    quality_standard = models.CharField('质量标准', max_length=80, blank=True)  # 如：法定标准、企业标准、国家药典、行业标准、地方标准等。
    dosage_form = models.CharField('剂型', max_length=20, blank=True)  # 如：片剂，胶囊剂，颗粒剂
    is_auth = models.NullBooleanField('是否已认证', blank=True, null=True)
    # is_qualified = models.NullBooleanField('是否检验合格', blank=True, null=True)
    is_otc = models.NullBooleanField('是否OTC', blank=True, null=True)
    is_zybh = models.NullBooleanField('是否中药保护品种', blank=True, null=True)
    is_new = models.NullBooleanField('是否新药', blank=True, null=True)  # 新药：未曾在中国境内上市销售的药品。
    is_oem = models.NullBooleanField('是否委托加工', blank=True, null=True)
    otc_type = models.IntegerField('OTC类型', choices=OTC_TYPE_CHOICES, blank=True, null=True)
    recipe_type = models.CharField('处方类型', max_length=30, blank=True)
    suitable_crowd = models.CharField('适用人群', max_length=30, blank=True)
    # desc = models.TextField('药品说明书', blank=True)
    # desc = RichTextField('药品说明书', blank=True, config_name = 'full')
    desc_drug = RichTextUploadingField('药品详情', blank=True, config_name='full')
    desc_good = RichTextUploadingField('药品说明书', blank=True, config_name='full')
    storage_condition = models.CharField('贮藏条件', max_length=30, blank=True)


class DosageForm(models.Model):
    """药品剂型"""
    name = models.CharField('剂型名称', max_length=20)

    def __unicode__(self):
        return self.name


class GoodQualification(models.Model):
    """产品资质文件"""
    good = models.ForeignKey(Good, verbose_name='产品', on_delete=models.CASCADE)
    photo = models.ImageField('图片', upload_to='qualification/good/%Y/%m/%d/')
    upload_man = models.ForeignKey(User, verbose_name='上传人', on_delete=models.CASCADE)
    upload_time = models.DateTimeField('上传时间', auto_now=True)


class GoodPhoto(models.Model):
    """产品照片"""
    good = models.ForeignKey(Good, verbose_name='产品', on_delete=models.CASCADE)
    photo = models.ImageField('图片', upload_to='good/%Y/%m/%d/')
    order_no = models.IntegerField('显示排序', blank=True, null=True)
    upload_man = models.ForeignKey(User, verbose_name='上传人', on_delete=models.CASCADE)
    upload_time = models.DateTimeField('上传时间', auto_now=True)


class PurchaseAgreementItem(models.Model):
    """采购协议清单"""
    agreement = models.ForeignKey(PurchaseAgreement, verbose_name='协议', on_delete=models.CASCADE)
    good = models.ForeignKey(Good, verbose_name='产品', on_delete=models.CASCADE)
    agree_price = models.IntegerField('协议价')  # 单位为 分


class LackRegister(models.Model):
    """缺货登记"""
    people = models.ForeignKey(User, verbose_name='登记人', on_delete=models.CASCADE)
    good = models.ForeignKey(Good, verbose_name='产品', on_delete=models.CASCADE)
    created = models.DateTimeField('登记时间', auto_now_add=True)
    note = models.TextField('备注', blank=True)
