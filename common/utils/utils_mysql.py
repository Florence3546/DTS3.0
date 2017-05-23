# coding=UTF-8
'''
针对MySQL数据库的处理工具类，包含SQL、表、字段操作
Created on 2011-09-07
@author: zhangyu
'''
import math

from django.conf import settings
from django.core.management import color
from django.core.management.color import no_style
from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.db import connection, models, transaction

from common.utils.utils_collection import genr_sublist
from common.utils.utils_error import SQLException
from common.utils.utils_log import log


def create_table_by_model(table_suffix, model_class, ref_model_list, engine_type = ''):
    '''根据静态Model、表名后缀、静态Model的关联其它Model创建一个表'''
    try:
        # 检查表是否已存在
        org_db_table = model_class._meta.db_table
        table_name = org_db_table + "_" + str(table_suffix)
        if table_name and is_table_exist(table_name):
            log.info("table %s already exist" % (table_name))
            return True
    except Exception, e:
        log.error('check table exist error, table_name=%s, e=%s' % (table_name, e))
        return False

    style = no_style()
    pending_references = {}
    cursor = connection.cursor()
    model_class._meta.db_table = table_name

    # 获取建表和关联sql
    sql, references = connection.creation.sql_create_model(model_class, style, set(ref_model_list))
    for refto, refs in references.items():
        pending_references.setdefault(refto, []).extend(refs)
        if refto in ref_model_list:
            sql.extend(connection.creation.sql_for_pending_references(refto, style, pending_references))
        else:
            log.error("Parameter error, %s does not reference Model： %s, Please check parameter: ref_model_list" % (model_class, ref_model_list))
            return False
    sql.extend(connection.creation.sql_for_pending_references(model_class, style, pending_references))

    if engine_type != '' and len(sql) > 0:
        sql[0] = sql[0][0:-2] + 'engine=' + engine_type + '\n' + ';'
    # 获取索引sql
    index_sql = connection.creation.sql_indexes_for_model(model_class, style)
    if index_sql:
        sql.extend(index_sql)

    model_class._meta.db_table = org_db_table
    log.info("Creating table %s ......, Model is %s" % (table_name, model_class))
    try:
        for statement in sql:
            cursor.execute(statement) # 执行脚本
    except Exception, e:
        log.exception("SQL Statement execute error, e=%s" % (e))
        return False

    log.info("Create table %s success" % (table_name))
    return True

# @transaction.commit_manually
def bulk_update_for_sql(sql, value_list, commit_number = 1000):
    '''批量执行sql语句保存数据，按照commit_number将value_list分组批量更新'''
    rowcount = 0
    for group_value_list in genr_sublist(value_list, commit_number):
        if group_value_list:
            try:
                cursor = connection.cursor()
                for temp_list in group_value_list:
                    rowcount += cursor.executemany(sql, temp_list) # sql语句里的字符串型参数 %s 两旁不加引号！
                    transaction.commit()
            except Exception, e:
                log.exception("SQL update error, e=%s" % (e))
                transaction.rollback()
                raise e
    return rowcount

# @transaction.commit_manually
def bulk_update_for_model(obj_list, commit_number = 1000):
    '''批量更新model_list数据，按照commit_number将obj_list分组批量更新'''
    for temp_list in genr_sublist(obj_list, commit_number):
        try:
            for obj in temp_list:
                obj.save(False, False)
            transaction.commit()
        except Exception, e:
            log.exception("Object save error, e=%s" % (e))
            transaction.rollback()
            raise e
    return len(obj_list)

def bulk_insert_for_model(objs, table_name = None, commit_number = 1000):
    '''用Bulk insert方式批量插入model list，按照commit_number分组批量插入'''
    if not objs:
        return 0
    rowcount = 0
    field_list = []
    model_class = objs[0].__class__
    if not table_name:
        table_name = model_class._meta.db_table
    for tmp_field in model_class._meta.fields:
        if isinstance(tmp_field, models.ForeignKey):
            field_list.append(tmp_field.name + "_id")
        else:
            field_list.append(tmp_field.name)

    qn = connection.ops.quote_name
    field_string = ', '.join([qn(field_name) for field_name in field_list])

    len_objs = len(objs)
    if len_objs > commit_number:
        exe_times = int(math.ceil(float(len_objs) / commit_number))
        for times in range(exe_times):
            tmp_objs = objs[commit_number * times:commit_number * (times + 1)]
            rowcount += __insert_for_model(table_name, field_string, field_list, tmp_objs)
    else:
        rowcount = __insert_for_model(table_name, field_string, field_list, objs)
    return rowcount

def __insert_for_model(table_name, field_string, field_list, objs):
    '''将Model中field_list对应的model objs批量插入'''
    values_list = []
    for obj in objs:
        for field_name in field_list:
            field_value = getattr(obj, field_name)
            values_list.append(field_value)

    arg_string = ', '.join([u'(' + ', '.join(['%s'] * len(field_list)) + ')'] * len(objs))
    sql = "INSERT INTO %s (%s) VALUES %s" % (table_name, field_string, arg_string,)

    try:
        cursor = connection.cursor()
        cursor.execute(sql, values_list)
        # transaction.commit_unless_managed()
    except Exception, e:
        log.exception("SQL Statement execute error, table_name=%s, e= %s" % (table_name, e))
        raise e
    return cursor.rowcount

def bulk_insert_for_dict(table_name, objs, field_list, commit_number = 1000):
    '''
    \用Bulk insert方式批量插入字典list，按照commit_number分组批量插入
    field_list格式为list=[field_name1,field_name2]
    objs格式为字典list=[{field_name1:value1,field_name2:value2,……},{……}]
    '''
    if not objs:
        return 0
    rowcount = 0
    qn = connection.ops.quote_name
    field_string = ', '.join([qn(field_name) for field_name in field_list])

    len_objs = len(objs)
    if len_objs > commit_number:
        exe_times = int(math.ceil(float(len_objs) / commit_number))
        for times in range(exe_times):
            tmp_objs = objs[commit_number * times:commit_number * (times + 1)]
            rowcount += __insert_for_dict(table_name, field_string, field_list, tmp_objs)
    else:
        rowcount = __insert_for_dict(table_name, field_string, field_list, objs)
    return rowcount

def __insert_for_dict(table_name, field_string, field_list, objs):
    '''将field_list对应的字典list objs批量插入'''
    values_list = []
    for obj in objs:
        for field_name in field_list:
            field_value = obj[field_name]
            values_list.append(field_value)

    arg_string = ', '.join([u'(' + ', '.join(['%s'] * len(field_list)) + ')'] * len(objs))
    sql = "INSERT INTO %s (%s) VALUES %s" % (table_name, field_string, arg_string,)

    try:
        cursor = connection.cursor()
        cursor.execute(sql, values_list)
        # transaction.commit_unless_managed()
    except Exception, e:
        log.exception("SQL Statement execute error, e=%s" % (e))
        raise e
    return cursor.rowcount

def execute_manage_sql(sql, value_list = None):
    '''
    \传入SQL执行插入、更新、删除、truncate操作，返回操作成功的记录条数

    replace说明：因为replace会先删除已存在的原记录，再插入记录，因此objs以及其对应的table必须满足如下条件才能调用：
    1、objs对象的属性不能被其他Model作为外键引用
    2、objs对象必须有单一主键或唯一索引
    3、objs对象的主键不能是自增长的id
    value_list、auto_commit可以为空，auto_commit=False时，需要在该函数外面做数据库提交
    '''
    script_type = None
    if sql:
        script_type = sql.lstrip()
        script_type = script_type[0:script_type.find(" ")].lower()
    try:
        if script_type in ["insert", "update", "delete", "truncate", "drop", "alter", "replace"]:
            # SQL语句格式："UPDATE bar SET foo = 1 WHERE baz = %s AND name = %s"
            cursor = connection.cursor()
            if not value_list:
                cursor.execute(sql)
            else:
                cursor.execute(sql, value_list)
            # if auto_commit:
            #     transaction.commit_unless_managed()
            return cursor.rowcount
        else:
            raise SQLException, "SQL syntax error：[%s]" % sql
    except Exception, e:
        log.exception("SQL Statement execute error, e=%s" % (e))
        raise e
    return True

def execute_query_sql(sql, value_list = None, model_class = None):
    '''
    \传入SQL执行数据库查询操作，返回结果可以是dict_list，也可以是model_list；

    value_list、model_class可以为空，model_class=None时，返回dict_list；
    model_class为模型对象时，返回model_list，如果model_class不包含ResultSet的属性，则会将该属性加入到model对象中；
    \查询时取了所有结果，如果数据量太大，需要在SQL语句中包含limit分页；
    \该函数用于替代RawSQL，但不同的是调用会立即执行查询，如果真的想只在使用对象时查询，就可以使用RawSQL，其它情况下慎用
    '''
    script_type = None
    if sql:
        script_type = sql.lstrip()
        script_type = script_type[0:script_type.find(" ")].lower()
    try:
        if script_type == "select":
            # SQL语句格式："SELECT foo FROM bar WHERE baz = %s AND name = %s LIMIT %s, %s"
            cursor = connection.cursor()
            if not value_list:
                cursor.execute(sql)
            else:
                cursor.execute(sql, value_list)
            # 得到查询的列属性和结果
            descr = cursor.description
            result_set = cursor.fetchall()
            # 将结果组装为字典列表
            if model_class == None:
                return [dict(zip([column[0] for column in descr], row)) for row in result_set]
            # 将结果组装为模型列表
            else:
                model_obj_list = []
                for row in result_set:
                    model_obj = model_class()
                    tuple_kv_list = zip([column[0] for column in descr], row)
                    for tuple_kv in tuple_kv_list:
                        setattr(model_obj, tuple_kv[0], tuple_kv[1])
                    model_obj_list.append(model_obj)
                return model_obj_list
        else:
            raise SQLException, "SQL syntax error：[%s]" % sql
    except Exception, e:
        log.exception("SQL Statement execute error, e=%s" % (e))
        raise e
    return None

def paginate_for_sql(count_sql, query_sql, page_no, page_size, all_count = None, recount = False):
    '''
    \根据SQL分页查询数据

    count_sql格式：SELECT %s FROM auth_user order by shop_id
    query_sql格式：SELECT username FROM auth_user order by shop_id
    \注意：1)要保证django/core/paginator.py中有后来添加的for_sql函数
    2)只有page_no=1或recount=True(需要每次都计算)的时候，才计算all_count，
    \其它情况需传入all_count(从page_obj.paginator.count中获取)，因此当翻页查询后，还有添加、删除操作时，应该设置recount=True
    '''
    this_page = None
    if page_no < 1 or page_size < 1 or not count_sql or not query_sql:
        return this_page
    try:
        if page_no == 1 or recount:
            count_sql = count_sql % ("count(*) all_count")
            all_count = execute_query_sql(count_sql)[0]["all_count"]

        query_sql += " LIMIT %s OFFSET %s" % (page_size, (page_no - 1) * page_size)
        data_list = execute_query_sql(query_sql)
        try:
            paginator = Paginator(data_list, page_size)
            this_page = paginator.page(1)
            this_page.for_sql(page_no, all_count)
        except (EmptyPage, InvalidPage):
            this_page = paginator.page(1)
            this_page.for_sql(1, all_count)
    except Exception, e:
        log.exception("page_no=%s, page_size=%s, all_count=%s, e=%s" % (page_no, page_size, all_count, e))
        raise e
    return this_page

def create_custom_model(name, fields = None, app_label = '', module = '', options = None, admin = None):
    '''生成动态模型'''
    class Meta:
        # Using type('Meta', ...) gives a dictproxy error during model creation
        pass
    if app_label:
        # app_label must be set using the Meta inner class
        setattr(Meta, 'app_label', app_label)
    # Update Meta with any options that were provided
    if options is not None:
        for key, value in options.items():
            setattr(Meta, key, value)
    # Set up a dictionary to simulate declarations within a class
    attrs = {'__module__': module, 'Meta': Meta}
    # Add in any fields that were provided
    if fields:
        attrs.update(fields)
    # Create an Admin inner class if admin options were provided
    if admin is not None:
        class Admin:
            pass
        for key, value in admin:
            setattr(Admin, key, value)
        attrs['Admin'] = Admin
    # Create the class, which automatically triggers ModelBase processing
    return type(str(name), (models.Model,), attrs)

def install_custom_model_to_db(custom_model):
    '''创建动态模型'''
    try:
        # 检查表是否已存在
        table_name = custom_model._meta.db_table
        if table_name and is_table_exist(table_name):
            return True
    except Exception, e:
        log.error('check table exist error, table_name=%s, e=%s' % (table_name, e))
        return False

    try:
        # 创建表
        style = color.no_style()
        cursor = connection.cursor()
        statements, pending = connection.creation.sql_create_model(custom_model, style)
        for sql in statements:
            cursor.execute(sql)
    except Exception, e:
        log.error("create model error, statements=%s, e=%s" % (statements, e))
        return False

    try:
        # 创建索引
        index_sql = connection.creation.sql_indexes_for_model(custom_model, style)
        for sql in index_sql:
            cursor.execute(sql)
    except Exception, e:
        log.error("create index error, index_sql=%s, e=%s" % (index_sql, e))
        return False
    return True

def is_table_exist(table_name, table_schema = None):
    '''检查数据库表是否已经存在'''
    table_exist = False
    if not table_schema:
        table_schema = settings.DATABASES["default"]["NAME"]
    if table_schema and table_name:
        table_check_sql = "SELECT table_name FROM information_schema.tables WHERE table_schema='%s' AND table_name='%s'" % (table_schema, table_name)
        cursor = connection.cursor()
        cursor.execute(table_check_sql)
        result = cursor.fetchall()
        if result:
            table_exist = True
    return table_exist

def execute_query_sql_return_tuple(sql):
    '''执行查询sql，直接返回tuple；限制：1、限于执行查询语句；2、直接返回tuple结果'''
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception, e:
        log.error('query tuple error, sql=%s, e=%s' % (sql, e))
        return ()
