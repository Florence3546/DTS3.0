# coding=UTF-8
from django.core.management.base import BaseCommand
from django.db import transaction

from common.utils import utils_mssql, utils_string
from common.utils.utils_log import log
from common.constant import ONLINE_YES
import datetime


class Command(BaseCommand):
    help = '根据时空中间数据库里的数据初始化DTS数据'

    def migrate_BUSINESSDOC(self):
        from dtsauth.models import Enterprise
        select_sql = '''
        select TOP %s BUSINESSID, BUSINESSNAME, TAXNO, BANKACCOUNT, CONTACT, [ADDRESS], TELEPHONE, URL, EMAIL, POSTCODE,
        BUSINESSCONT, FAX, REGAUTHORITY, REGDATES, REGVALDATE, SUBBRANCH, REGCAPITAL, OPERMODE, REGNO, LEGALREP, ORGCERT
        from dts.dbo.BUSINESSDOC;
        ''' % self.ROWS_TOP
        delete_sql = 'delete top (%s) from dts.dbo.BUSINESSDOC;' % self.ROWS_TOP
        mssql_field_map = {
            'external_id': 'BUSINESSID',
            'name': 'BUSINESSNAME',
            'short_name': 'BUSINESSNAME',
            'pinyin': 'BUSINESSNAME',
            'biz_scope': 'BUSINESSCONT',
            'address': 'ADDRESS',
            'subbranch': 'SUBBRANCH',
            'bank_account': 'BANKACCOUNT',
            'reg_capital': 'REGCAPITAL',
            'operate_mode': 'OPERMODE',
            'reg_no': 'REGNO',
            'org_code': 'ORGCERT',
            'legal_repr': 'LEGALREP',
            'reg_authority': 'REGAUTHORITY',
            'valid_from': 'REGDATES',
            'valid_to': 'REGVALDATE',
            'contact': 'CONTACT',
            'phone': 'TELEPHONE',
            'website': 'URL',
            'email': 'EMAIL',
            'fax': 'FAX',
        }
        while True:
            self.mssql_cursor.execute(select_sql)
            rows = self.mssql_cursor.fetchall()
            if not rows:
                break
            data_list = []
            for row in rows:
                temp_data = {k: row.get(v) or '' for k, v in mssql_field_map.items()}
                temp_data['is_master'] = False
                if temp_data.get('pinyin'):
                    temp_data['pinyin'] = utils_string.get_pinyin_code(temp_data['pinyin'])
                if temp_data.get('valid_from'):
                    try:
                        temp_data['valid_from'] = datetime.datetime.strptime(temp_data['valid_from'].strip()[:10], '%Y-%m-%d')
                    except Exception, e:
                        log.error('python manage.py init_ksoa_data migrate_BUSINESSDOC valid_from error: %s, valid_from=%s' % (e, temp_data['valid_from']))
                        temp_data['valid_from'] = None
                else:
                    temp_data['valid_from'] = None
                if temp_data.get('valid_to'):
                    try:
                        temp_data['valid_to'] = datetime.datetime.strptime(temp_data['valid_to'].strip()[:10], '%Y-%m-%d')
                    except Exception, e:
                        log.error('python manage.py init_ksoa_data migrate_BUSINESSDOC valid_to error: %s, valid_to=%s' % (e, temp_data['valid_to']))
                        temp_data['valid_to'] = None
                else:
                    temp_data['valid_to'] = None
                data_list.append(temp_data)
            try:
                with transaction.atomic():
                    Enterprise.objects.bulk_create([Enterprise(**data) for data in data_list])
                    self.mssql_cursor.execute(delete_sql)
                    self.mssql_conn.commit()
            except Exception, e:
                log.error('python manage.py init_ksoa_data migrate_BUSINESSDOC bulk_create error: %s' % e)
                for data in data_list:
                    try:
                        Enterprise.objects.update_or_create(external_id=data['external_id'], defaults=data)
                        self.mssql_cursor.execute("delete from dts.dbo.BUSINESSDOC where BUSINESSID='%s';" % data['external_id'])
                    except Exception, e:
                        log.error('python manage.py init_ksoa_data migrate_BUSINESSDOC update_or_create error: %s, external_id=%s' % (e, data['external_id']))

    def migrate_ENTDOC(self):
        from dtsauth.models import Enterprise
        select_sql = '''
        select TOP %s ENTID, ENTNAME, TELEPHONE, [ADDRESS], INDUSTRYTYPE, ENTTYPE, BEACTIVE, SYSMASTER, ISFREEZE, ISLEGAL
        from dts.dbo.ENTDOC;
        ''' % self.ROWS_TOP
        delete_sql = 'delete top (%s) from dts.dbo.ENTDOC;' % self.ROWS_TOP
        mssql_field_map = {
            'external_id': 'ENTID',
            'name': 'ENTNAME',
            'short_name': 'ENTNAME',
            'pinyin': 'ENTNAME',
            'address': 'ADDRESS',
            'operate_mode': 'INDUSTRYTYPE',
            'phone': 'TELEPHONE',
            'economic_type': 'ENTTYPE',
            'is_master': 'SYSMASTER',
        }
        while True:
            self.mssql_cursor.execute(select_sql)
            rows = self.mssql_cursor.fetchall()
            if not rows:
                break
            data_list = []
            for row in rows:
                temp_data = {k: row.get(v) or '' for k, v in mssql_field_map.items()}
                if temp_data.get('pinyin'):
                    temp_data['pinyin'] = utils_string.get_pinyin_code(temp_data['pinyin'])
                if temp_data.get('is_master') == 'Y':
                    temp_data['is_master'] = True
                else:
                    temp_data['is_master'] = False
                data_list.append(temp_data)
            try:
                with transaction.atomic():
                    Enterprise.objects.bulk_create([Enterprise(**data) for data in data_list])
                    self.mssql_cursor.execute(delete_sql)
                    self.mssql_conn.commit()
            except Exception, e:
                log.error('python manage.py init_ksoa_data migrate_ENTDOC bulk_create error: %s' % e)
                for data in data_list:
                    try:
                        Enterprise.objects.update_or_create(external_id=data['external_id'], defaults=data)
                        self.mssql_cursor.execute("delete from dts.dbo.ENTDOC where ENTID='%s';" % data['external_id'])
                    except Exception, e:
                        log.error('python manage.py init_ksoa_data migrate_ENTDOC update_or_create error: %s, external_id=%s' % (e, data['external_id']))

    def migrate_GOODSDOC(self):
        from good.models import Good
        select_sql = '''
        select TOP %s GOODSID, BARCODE, GOODSNAME, GOODSSPEC, MANUFACTURER
        from dts.dbo.GOODSDOC;
        ''' % self.ROWS_TOP
        delete_sql = 'delete top (%s) from dts.dbo.GOODSDOC;' % self.ROWS_TOP
        mssql_field_map = {
            'external_id': 'GOODSID',
            'name': 'GOODSNAME',
            'trade_name': 'GOODSNAME',
            'pinyin': 'GOODSNAME',
            'external_spec': 'GOODSSPEC',
            'manufacturer': 'MANUFACTURER',
            'barcode': 'BARCODE',
        }
        while True:
            self.mssql_cursor.execute(select_sql)
            rows = self.mssql_cursor.fetchall()
            if not rows:
                break
            data_list = []
            for row in rows:
                temp_data = {k: row.get(v) or '' for k, v in mssql_field_map.items()}
                temp_data['is_online'] = ONLINE_YES
                temp_data['online_time'] = datetime.datetime.now()
                if temp_data.get('pinyin'):
                    temp_data['pinyin'] = utils_string.get_pinyin_code(temp_data['pinyin'])
                    temp_data['pinyin_tn'] = temp_data['pinyin']
                data_list.append(temp_data)
            try:
                with transaction.atomic():
                    Good.objects.bulk_create([Good(**data) for data in data_list])
                    self.mssql_cursor.execute(delete_sql)
                    self.mssql_conn.commit()
            except Exception, e:
                log.error('python manage.py init_ksoa_data migrate_GOODSDOC bulk_create error: %s' % e)
                for data in data_list:
                    try:
                        Good.objects.update_or_create(external_id=data['external_id'], defaults=data)
                        self.mssql_cursor.execute("delete from dts.dbo.GOODSDOC where GOODSID='%s';" % data['external_id'])
                    except Exception, e:
                        log.error('python manage.py init_ksoa_data migrate_GOODSDOC update_or_create error: %s, external_id=%s' % (e, data['external_id']))

    def migrate_GOODSATTR(self):
        from good.models import Good, DrugAttr
        select_sql = '''
        select TOP %s GOODSID, SALETYPE, GCATEGORY, QCATEGORY, APPROVALNO, APPROVALDATE, APPROVALTO, FORMULA, QUALSTAND,
        STORAGETERM, RecipeType, bzjs
        from dts.dbo.GOODSATTR;
        ''' % self.ROWS_TOP
        delete_sql = 'delete top (%s) from dts.dbo.GOODSATTR;' % self.ROWS_TOP
        mssql_field_map = {
            'external_id': 'GOODSID',
            'license': 'APPROVALNO',
            'valid_from': 'APPROVALDATE',
            'valid_to': 'APPROVALTO',
            'quality_standard': 'QUALSTAND',
            'dosage_form': 'FORMULA',
            'recipe_type': 'RecipeType',
            'storage_condition': 'STORAGETERM',
        }
        good_field_map = {
            'external_id': 'GOODSID',
            'external_category': 'GCATEGORY',
            'extra_category': 'QCATEGORY',
        }

        while True:
            self.mssql_cursor.execute(select_sql)
            rows = self.mssql_cursor.fetchall()
            if not rows:
                break
            external_id_list = [row['GOODSID'] for row in rows if row.get('GOODSID')]
            good_id_dict = dict(Good.objects.filter(external_id__in=external_id_list).values_list('external_id', 'id'))
            data_list = []
            for row in rows:
                temp_data = {k: row.get(v) or '' for k, v in mssql_field_map.items()}
                temp_data['good_id'] = good_id_dict.get(temp_data['external_id'])
                if temp_data.get('valid_from'):
                    try:
                        temp_data['valid_from'] = datetime.datetime.strptime(temp_data['valid_from'][:10].strip(), '%Y-%m-%d')
                    except Exception, e:
                        log.error('python manage.py init_ksoa_data migrate_GOODSATTR valid_from error: %s, valid_from=%s' % (e, temp_data['valid_from']))
                        temp_data['valid_from'] = None
                else:
                    temp_data['valid_from'] = None
                if temp_data.get('valid_to'):
                    try:
                        temp_data['valid_to'] = datetime.datetime.strptime(temp_data['valid_to'][:10].strip(), '%Y-%m-%d')
                    except Exception, e:
                        log.error('python manage.py init_ksoa_data migrate_GOODSATTR valid_to error: %s, valid_to=%s' % (e, temp_data['valid_to']))
                        temp_data['valid_to'] = None
                else:
                    temp_data['valid_to'] = None
                data_list.append(temp_data)
                temp_good_data = {k: row.get(v) or '' for k, v in good_field_map.items()}
                Good.objects.filter(external_id=temp_good_data['external_id']).update(**temp_good_data)
            try:
                with transaction.atomic():
                    DrugAttr.objects.bulk_create([DrugAttr(**data) for data in data_list])
                    self.mssql_cursor.execute(delete_sql)
                    self.mssql_conn.commit()
            except Exception, e:
                log.error('python manage.py init_ksoa_data migrate_GOODSATTR bulk_create error: %s' % e)
                for data in data_list:
                    try:
                        DrugAttr.objects.update_or_create(external_id=data['external_id'], defaults=data)
                        self.mssql_cursor.execute("delete from dts.dbo.GOODSATTR where GOODSID='%s';" % data['external_id'])
                    except Exception, e:
                        log.error('python manage.py init_ksoa_data migrate_GOODSATTR update_or_create error: %s, external_id=%s' % (e, data['external_id']))

    def migrate_EGBALANCE(self):
        from good.models import Good
        select_sql = '''
        select TOP %s GOODSID, STORNUM from dts.dbo.EGBALANCE;
        ''' % self.ROWS_TOP
        delete_sql = 'delete top (%s) from dts.dbo.EGBALANCE;' % self.ROWS_TOP
        mssql_field_map = {
            'external_id': 'GOODSID',
            'stock_amount': 'STORNUM',
        }
        while True:
            self.mssql_cursor.execute(select_sql)
            rows = self.mssql_cursor.fetchall()
            if not rows:
                break
            for row in rows:
                temp_data = {k: row.get(v) or '' for k, v in mssql_field_map.items()}
                if temp_data.get('stock_amount'):
                    try:
                        temp_data['stock_amount'] = int(temp_data['stock_amount'])
                    except Exception, e:
                        log.error('python manage.py init_ksoa_data migrate_EGBALANCE stock_amount error: %s, stock_amount=%s' % (e, temp_data['stock_amount']))
                        temp_data['stock_amount'] = None
                else:
                    temp_data['stock_amount'] = None
                Good.objects.filter(external_id=temp_data['external_id']).update(**temp_data)
            self.mssql_cursor.execute(delete_sql)
            self.mssql_conn.commit()

    def migrate_PGRICE(self):
        from good.models import Good
        select_sql = '''
        select TOP %s GOODSID, UNIT, SALEP from dts.dbo.PGPRICE;
        ''' % self.ROWS_TOP
        delete_sql = 'delete top (%s) from dts.dbo.PGPRICE;' % self.ROWS_TOP
        mssql_field_map = {
            'external_id': 'GOODSID',
            'unit': 'UNIT',
            'retail_price': 'SALEP',
        }
        while True:
            self.mssql_cursor.execute(select_sql)
            rows = self.mssql_cursor.fetchall()
            if not rows:
                break
            for row in rows:
                temp_data = {k: row.get(v) or '' for k, v in mssql_field_map.items()}
                if temp_data.get('retail_price'):
                    try:
                        temp_data['retail_price'] = int(temp_data['retail_price']*100)
                        temp_data['member_price'] = temp_data['retail_price']
                    except Exception, e:
                        log.error('python manage.py init_ksoa_data migrate_PGRICE retail_price error: %s, retail_price=%s' % (e, temp_data['retail_price']))
                        temp_data['retail_price'] = None
                        temp_data['member_price'] = None
                else:
                    temp_data['retail_price'] = None
                    temp_data['member_price'] = None
                Good.objects.filter(external_id=temp_data['external_id']).update(**temp_data)
            self.mssql_cursor.execute(delete_sql)
            self.mssql_conn.commit()

    def handle(self, *args, **options):
        self.mssql_conn = utils_mssql.get_conn('dts')
        self.mssql_cursor = self.mssql_conn.cursor(as_dict=True)
        self.ROWS_TOP = 100

        # self.migrate_BUSINESSDOC()
        # self.migrate_ENTDOC()
        # self.migrate_GOODSDOC()
        # self.migrate_GOODSATTR()
        # self.migrate_EGBALANCE()
        # self.migrate_PGRICE()

        self.mssql_cursor.close()
        self.mssql_conn.close()
