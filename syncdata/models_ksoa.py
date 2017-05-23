# coding=UTF-8
from __future__ import unicode_literals
from common.utils import utils_mssql
from django.db import models

"""
用友时空进销存软件同步模块
"""


class BaseData(object):

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class GOODSDOC(BaseData):
    """商品基础资料"""
    ENTID = '企业ID'
    GOODSID = '商品ID'
    BRANDID = ''
    ISNEW = ''
    ISFREEZE = ''
    ISABANDON = ''
    BAACTIVE = ''
    BARCODE = '条形码'
    GOODSCODE = '商品编号'
    OLDCODE = ''
    GOODSNAME = '商品通用名'
    FOREIGNNAME = ''
    SHORTNAME = ''
    LOGOGRAM = '助记码'
    GOODSSPEC = '商品规格'
    PLACE = '厂家地址'
    MANUFACTURER = '生产厂家'
    GOODSDESC = ''
    CREATETIME = '创建时间'
    DOCLEVID = ''
    CREATERID = ''
    CREATERINFO = ''
    LASTMODIFYTIME = '最近修改时间'
    DELUSERID = ''
    DELTIME = ''
    EXPAUTORG = ''
    RESAUTORG = ''
    BILLNO = ''
    ISPASS = ''
    CHECKCOST = ''
    MFCID = ''
    LASTSTFID = ''
    LASTREVTIME = ''
    COUNTRYID = ''
    ISIMPORTED = ''
    BusinessId = ''
    dah = ''
    swflbm = ''
    sfswyh = ''
    scxkz = ''


class GOODSATTR(BaseData):
    """商品核心属性"""
    GOODSID = '商品ID'
    ENTID = '企业ID'
    SALETYPE = '销售性质'
    ISMATERIEL = ''
    ISAUXIL = ''
    ISTOOLS = ''
    ISASSETS = ''
    ISSERV = ''
    ISFREE = ''
    ISGIFT = ''
    ISSTOCKS = ''
    HESID = ''
    ACCTLEVEL = ''
    ISANGLE = ''
    ANGLETYPE = ''
    SCHEMAID = ''
    YEARSNUM = ''
    SEASON = ''
    FABRIC = ''
    ACCES = ''
    APPEARDATE = ''
    EXITDATE = ''
    LIFETYPE = ''
    CONVRATIO = ''
    INTAXRATE = '进项税率'
    OUTTAXRATE = '销项税率'
    RETAILP = ''
    KEMU = ''
    ISGOODS = ''
    BILLNO = ''
    ISPASS = ''
    GENERALNAME = ''
    CHEMNAME = ''
    COMMNAME = ''
    GCATEGORY = '经营范围'
    ISGSP = ''
    ISGMP = ''
    ISFIRST = ''
    ISHERBAL = ''
    ISTRAD = ''
    APPROVALNO = '批准文号'
    FORMULA = '剂型'
    ISPSY = ''
    ISMEDICARE = ''
    ISREFRIG = ''
    EXPRICE = ''
    QUALSTAND = '质量标准'
    ISSALE = ''
    ISPROCUR = ''
    ISCONTROL = ''
    ISMAIN = ''
    ISPROM = ''
    MAXRETAIP = ''
    MINRETAIP = ''
    ADRETAILP = ''
    MEMPRICE = ''
    MANAGEPACK = ''
    SALEP = ''
    PURP = ''
    BIDDPRICE = ''
    PURTAXP = ''
    SALETAXP = ''
    MINSALEP = ''
    MAXSALEP = ''
    LIMITPURP = ''
    ISCOSTACCT = ''
    INTERSCA = ''
    GENDER = ''
    PLANCATE = ''
    ISLIMIT = ''
    LIMITNUM = ''
    ISPRES = ''
    APPROVALDATE = '批准文号生效日期'
    APPROVALTO = '批准文号失效日期'
    ISDRUG = ''
    ISKEF = ''
    ISQA = ''
    INEFFECTDAY = ''
    DAYUNIT = ''
    DFTWHID = '库房存储条件'
    DFTLOCATID = '货位存储条件'
    CURCYCLE = ''
    ISTJ = ''
    TJ = ''
    STORAGETERM = '贮藏条件'
    ISELEC = ''
    ISDOUCHK = ''
    ISWITHPIC = ''
    REGMARK = ''
    DOWNPURP = ''
    LISTPRICE = ''
    QCATEGORY = '质量分类'
    INNERPRICE = ''
    REGMARKVALTO = ''
    ISBASEMED = ''
    SDATE = ''
    EDATE = ''
    WmsMeas = ''
    bzjs = '包装件数'
    RecipeType = '处方类型'
    k_ismhj = ''


class PGPRICE(BaseData):
    """商品包装单位"""
    PACKID = '商品包装ID'
    ENTID = '企业ID'
    GOODSID = '商品ID'
    UNIT = '包装单位'
    MEAS = '计量规格'
    BARCODE = '条形码'
    RETAILP = '零售价'
    ISBASE = ''
    ISPURPACK = ''
    ISRETPACK = ''
    MEMPRICE = '会员价'
    LENGTH = ''
    WIDE = ''
    HIGH = ''
    BULKS = ''
    WEIGHT = ''
    ISSALEPACK = ''
    SALEP = '标准售价'
    PURP = '标准进价'
    SALETAXP = '含税售价'
    PURTAXP = '含税进价'


class EGBALANCE(BaseData):
    """企业库存表"""
    GOODSID = '商品ID'
    ENTID = '企业ID'
    PLACEPACK = ''
    PLACENUM = '库管数量'
    STORPACK = ''
    STORNUM = '库存数量'
    STORAMOUNT = ''
    FINNUM = '财务库存数量'
    FINAMOUNT = ''
    STORMAX = ''
    STORMIN = ''
    STORFIT = ''
    OLDJS = ''
    OLDNUM = '基本数量'
    OLDAMOUNT = ''
    PREPACK = ''
    PRENUM = ''
    PREAMOUNT = ''
    PROFITRATE = ''
    FIXCOST = ''
    COST = '成本价'
    CARRCOST = ''
    MAXPURP = '最高进价'
    LASTPURP = ''
    MINPURP = '最低进价'
    FINPACK = ''


class ENTDOC(BaseData):
    """企业表"""
    ENTID = '企业ID'
    ENTINCODE = ''
    ENTCODE = ''
    ENTNAME = '企业名'
    FOREIGNNAME = ''
    LOGOGRAM = '拼音简写'
    ENTNO = ''
    TELEPHONE = '电话'
    ADDRESS = '地址'
    POSTCODE = '邮编'
    CONTACT = ''
    URL = ''
    EMAIL = ''
    FAX = ''
    INDUSTRY = ''
    INDUSTRYTYPE = '产业类型'  # 如：'批发'
    DOCLEVID = ''
    BEACTIVE = '是否激活'
    ENTLEVEL = ''
    LASTMODIFYTIME = '最后修改时间'
    CREATETIME = '创建时间'
    CREATERID = '创建者'  # 从时空导入的数据，创建者采用虚拟用户"用友时空"
    CREATERINFO = ''
    DELTIME = ''
    DELUSERID = ''
    ENTTYPE = '企业经济类型'  # 如：'股份'
    TEMPLETID = ''
    SYSMASTER = '是否是系统持有者'
    HIRESUM = ''
    ISFREEZE = '是否冻结'
    FREEZEDATE = '冻结日期'
    FREEZEREASON = '冻结原因'
    FREEZEDAYS = '冻结天数'
    OPENERID = '开启者ID'
    DAYPRICE = ''
    MONEYLIMIT = ''
    LIMITDAYS = ''
    REMINDDAYS = ''
    ENDDATE = ''
    LASTPAYDATE = ''
    BALANCE = '余额'
    DIRECTORID = ''
    SALEENTID = ''
    LASTLOGINTIME = '最后登录时间'
    POLICYASP = ''
    ASPUSERNUM = ''
    OPERASTATE = ''
    ASPNUM = ''
    ASPORGNUM = ''
    POLPRICE = ''
    CATCHWORD = ''
    QUESTION = ''
    ANSWER = ''
    USERID = ''
    ISPASS = ''
    AUDITDATE = ''
    AUDITUSERID = ''
    SUBSCRIPTION = ''
    ISLEGAL = '是否合法'
    ISDEVELOPER = ''
    ISSELLER = ''
    ISSERVPROV = ''
    ISCLUB = ''
    ISCONSUMER = ''
    ISFIRM = ''
    ISMAKER = ''
    DEVELOPERLEVEL = ''
    SERVENTLEVEL = ''
    ISASSOCIATOR = ''
    ASSOCIATORURL = ''
    CATALOG = ''
    LAYOUTID = ''
    ISUSE = ''
    ACCOUNTID = ''
    GRADE = ''
    TOTALPOINTS = ''
    STARTS = ''
    ATTACHID = ''
    CURRENCYID = ''
    ISLOCK = ''
    ENTSUPID = ''
    CATCODE = ''
    GROUPENTID = ''
    ISSINGLE = ''
    EXPAUTORG = ''
    RESAUTORG = ''
    ISORGALONE = ''
    USEENTID = ''
    ENTURL = ''
    ACCESSEDNUM = ''
    CONSLEVEL = ''
    VENLEVELID = ''
    ISOPER = ''
    ISCEASE = ''
    SYSENTID = ''
    REGUSERID = ''
    ISCONS = ''
    HYJH = ''
    DEVRATE = ''
    RATE = ''
    ENTDESC = ''
    QQ = ''
    FINADAY = ''
    FINAMONTH = ''
    ISQUARTER = ''
    DIMCODE = ''
    EVALUATION = ''
    INTRODUCE = ''
    TENET = ''
    SALELEVEL = ''
    MOBILE = ''
    SLOGAN = ''
    TYPEID = ''
    GPSADD = ''
    LASTBBSTIME = ''
    LOGO = ''


class BATCHCODE(BaseData):
    """批号表"""
    BATCHCODE = '批号'


class DICTDOC(BaseData):
    """字典表"""


class SUPPLYDOC(BaseData):
    """供应商表"""


class APGOODSDT(BaseData):
    """订单信息"""


class STOREROOM(BaseData):
    """库房货位表"""
    LOCATID = '货位ID'
    WHID = '库房ID'


class STOREHOUSE(BaseData):
    """库房表"""
    WHID = '库房ID'


class BUSINESSDOC(BaseData):
    """业务客户表"""
    BUSINESSID = '客户ID'
    ENTID = '企业ID'
    RFENTID = ''
    PBUSINESSID = ''
    BUSINESSCODE = ''
    BUSINESSNAME = '客户名'
    SHORTNAME = ''
    LOGOGRAM = '拼音简写'
    OLDCODE = ''
    TAXNO = '税务登记证号'
    BANKACCOUNT = '银行账号'
    CONTACT = '联系人'
    ADDRESS = '住所'
    TELEPHONE = '电话'
    URL = '企业官网'
    EMAIL = '联系邮箱'
    POSTCODE = '邮编'
    BUSINESSCONT = '经营范围'
    CONTENT = ''
    ORGID = ''
    DEPTID = ''
    INFOSTATE = ''
    DIRECTORID = ''
    ISBUSINESS = ''
    IS_SUPP = ''
    ISCLIENTS = ''
    ISLOGISTICS = ''
    LEVELID = ''
    ISABANDON = ''
    REASON = ''
    BEACTIVE = ''
    DOCLEVID = ''
    CREATERID = ''
    CREATERINFO = ''
    DELTIME = ''
    DELUSERID = ''
    LASTMODIFYTIME = ''
    BILLNO = ''
    ISPASS = ''
    GROUPID = ''
    CHANCEID = ''
    ZONEID = ''
    CREATETIME = ''
    EXPAUTORG = ''
    RESAUTORG = ''
    ISPARTNER = ''
    LASTDATE = ''
    PFBUSINESSID = ''
    FAX = '传真'
    REGAUTHORITY = '登记机关'
    REGDATES = '营业期限自'
    REGVALDATE = '营业期限至'
    SUBBRANCH = '开户支行'
    CZONEID = ''
    ISFREEZE = ''
    REGCAPITAL = '注册资本'
    OPERMODE = '经营类型'  # 批发 零售 医院 诊所 终端 医疗机构 非营利性医疗机构
    CAPACITY = ''
    REGNO = '机构登记证号'
    LEGALREP = '法定代表人'
    IDCARD = ''
    ISOPEN = ''
    SIGNDATE = ''
    ISCOMPASS = ''
    AUDITDATE = ''
    AUDITUSERID = ''
    SUBSCRIPTION = ''
    IS_TRAINPARTNER = ''
    HAS_TRAINDOC = ''
    K_TRAINCOST = ''
    K_TRAINSTARTDATE = ''
    K_TRAINENDDATE = ''
    CREATEDATE = ''
    ISREFER = ''
    YINGYZZ = ''
    ACCTNAME = ''
    ORGCERT = '统一社会信用代码/组织机构代码'
    ORGCERTDATE = ''
    ORGCERTVAL = ''
    IS_JOBCHAN = ''
    K_STAFFTYPE = ''
    REGYEARDATE = ''
    GPSADD = ''
    CENTID = ''
    RouteId = ''
    RouteOrder = ''
    b_boro_id = ''
    b_boro_name = ''
    b_city_id = ''
    b_city_name = ''
    dah = ''


class GoodsDoc(models.Model):
    """商品基础资料"""
    ent_id = models.CharField('企业ID', max_length=11, blank=True, db_column='ENTID')
    goods_id = models.CharField('商品ID', max_length=11, blank=True, db_column='GOODSID')
    barcode = models.CharField('条形码', max_length=50, blank=True, db_column='BARCODE')
    goods_name = models.CharField('通用名', max_length=120, blank=True, db_column='GOODSNAME')  # 如：对乙酰氨基酚
    goods_spec = models.CharField('制剂规格', max_length=100, blank=True, db_column='GOODSSPEC')  # 如：0.5g
    manufacturer = models.CharField('生产企业', max_length=256, blank=True, db_column='MANUFACTURER')

    class Meta:
        db_table = 'GOODSDOC'


class GoodsAttr(models.Model):
    """商品核心属性"""
    ent_id = models.CharField('企业ID', max_length=11, blank=True, db_column='ENTID')
    goods_id = models.CharField('商品ID', max_length=11, blank=True, db_column='GOODSID')
    sale_type = models.CharField('销售性质', max_length=6, blank=True, db_column='SALETYPE')
    g_category = models.CharField('经营范围', max_length=20, blank=True, db_column='GCATEGORY')
    q_category = models.CharField('质量分类', max_length=20, blank=True, db_column='QCATEGORY')
    approval_no = models.CharField('批准文号', max_length=36, blank=True, db_column='APPROVALNO')
    approval_date = models.DateField('批准文号生效日期', blank=True, db_column='APPROVALDATE')
    approval_to = models.DateField('批准文号失效日期', blank=True, db_column='APPROVALTO')
    formula = models.CharField('剂型', max_length=30, blank=True, db_column='FORMULA')
    qual_stand = models.CharField('质量标准', max_length=256, blank=True, db_column='QUALSTAND')
    storage_term = models.CharField('贮藏条件', max_length=256, blank=True, db_column='STORAGETERM')
    recipe_type = models.CharField('处方类型', max_length=256, blank=True, db_column='RecipeType')
    bzjs = models.IntegerField('包装件数', blank=True, null=True, db_column='bzjs')

    class Meta:
        db_table = 'GOODSATTR'


class PgPrice(models.Model):
    """商品包装单位"""
    ent_id = models.CharField('企业ID', max_length=11, blank=True, db_column='ENTID')
    goods_id = models.CharField('商品ID', max_length=11, blank=True, db_column='GOODSID')
    pack_id = models.CharField('商品包装ID', max_length=50, blank=True, db_column='PACKID')
    unit = models.CharField('包装单位', max_length=20, blank=True, db_column='UNIT')
    meas = models.IntegerField('计量规格', blank=True, null=True, db_column='MEAS')
    barcode = models.CharField('条形码', max_length=30, blank=True, db_column='BARCODE')
    retail_p = models.CharField('零售价', max_length=30, blank=True, db_column='RETAILP')
    mem_price = models.CharField('会员价', max_length=30, blank=True, db_column='MEMPRICE')

    class Meta:
        db_table = 'PGPRICE'


class EgBalance(models.Model):
    """企业库存表"""
    ent_id = models.CharField('企业ID', max_length=11, blank=True, db_column='ENTID')
    goods_id = models.CharField('商品ID', max_length=50, blank=True, db_column='GOODSID')
    place_num = models.IntegerField('库管数量', max_length=50, blank=True, db_column='PLACENUM')
    stor_num = models.IntegerField('库存数量', max_length=50, blank=True, db_column='STORNUM')

    class Meta:
        db_table = 'EGBALANCE'


class EntDoc(models.Model):
    """企业表"""
    ent_id = models.CharField('企业ID', max_length=11, blank=True, db_column='ENTID')
    ent_name = models.CharField('企业名', max_length=128, blank=True, db_column='ENTNAME')
    phone = models.CharField('联系电话', max_length=64, blank=True, db_column='TELEPHONE')
    address = models.TextField('地址', blank=True, db_column='ADDRESS')
    operate_mode = models.CharField('经营方式', max_length=128, blank=True, db_column='INDUSTRYTYPE')
    economic_type = models.CharField('企业经济类型', max_length=64, blank=True, db_column='ENTTYPE')
    be_active = models.CharField('是否激活', max_length=10, blank=True, db_column='BEACTIVE')
    is_master = models.CharField('是否是系统持有者', max_length=10, blank=True, db_column='SYSMASTER')
    is_lock = models.CharField('是否冻结', max_length=10, blank=True, db_column='ISFREEZE')
    is_legal = models.CharField('是否合法', max_length=10, blank=True, db_column='ISLEGAL')

    class Meta:
        db_table = 'ENTDOC'


class StoreRoom(models.Model):
    """库房货位表"""
    locat_id = models.CharField('货位ID', max_length=30, blank=True, db_column='LOCATID')
    wh_id = models.CharField('库房ID', max_length=30, blank=True, db_column='WHID')

    class Meta:
        db_table = 'STOREROOM'


