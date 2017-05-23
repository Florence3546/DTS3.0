# coding=UTF-8
from __future__ import unicode_literals

import datetime
import json
import uuid
from django.core.serializers.json import DjangoJSONEncoder
from django.core.cache import cache
from django.db import models
from common.utils.utils_log import log


class ProcessManager(models.Manager):
    """
    WARNING:
        创建工作流的唯一接口是 Process.objects.create_process(proc_type)；
        直接用Process(**kwargs)，或者Process.objects.create(**kwargs)，会因为参数设置不当导致流程异常!
    """

    def create_process(self, proc_type):
        proc_conf = self.model.get_proc_conf(proc_type)
        config = self.model.get_config(proc_conf)
        start_task = self.model.get_start_task(config)
        process = self.create(
            proc_type=proc_type,
            proc_conf=proc_conf,
            state_json=json.dumps({start_task: {
                'state': Task.TASK_IN_ORDER,
                'from': None,
                'can_reverse': False,
            }}, cls=DjangoJSONEncoder),
        )
        return process


class Process(models.Model):
    """
    业务流程模型
    state_json 格式:
    {
        task_name:{
            "state":state,
            "from":task_name,  # 上一个任务
            "can_reverse":True  # 能否撤销
            "updated": datetime  # 上次更新时间
            "org_kwargs": {}  # 原始数据
        }, ...
    }
    """

    # 定义类属性
    PROCESS_TYPE_DICT = {}                            # 流程类型字典
    PROCESS_TYPE_CHOICES = []
    PROCESS_CONFIG_DICT = {}                          # 流程配置字典
    PROCESS_CONFIG_CHOICES = []
    START_TASK = 'START_TASK'                         # 流程启动任务名
    END_TASK_LIST = 'END_TASK_LIST'                   # 流程终止任务名列表
    PROCESS_STATE_CACHE = 'PROCESS_STATE_%s'
    CACHE_TIMEOUT = 60*60*24                          # 单位为秒

    # 定义数据字段
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    proc_type = models.CharField('流程类型', max_length=50, choices=PROCESS_TYPE_CHOICES)
    proc_conf = models.CharField('流程配置', max_length=50, choices=PROCESS_CONFIG_CHOICES)
    state_json = models.CharField('运行状态字典', max_length=200)
    created = models.DateTimeField('创建时间', auto_now_add=True)
    ended = models.DateTimeField('结束时间', blank=True, null=True)

    objects = ProcessManager()

    def __unicode__(self):
        return '%s<%s>' % (self.proc_conf, self.id)

    @classmethod
    def register_type_dict(cls, type_dict):
        """注册可用的流程类型"""
        cls.PROCESS_TYPE_DICT = type_dict
        cls.PROCESS_TYPE_CHOICES = [(name, dic['name_cn']) for name, dic in type_dict.items()]
        cls.proc_type.choices = cls.PROCESS_TYPE_CHOICES

    @classmethod
    def register_config_dict(cls, config_dict):
        """注册可用的流程配置"""
        cls.PROCESS_CONFIG_DICT = config_dict
        cls.PROCESS_CONFIG_CHOICES = [(name, dic['name_cn']) for name, dic in config_dict.items()]
        cls.proc_conf.choices = cls.PROCESS_CONFIG_CHOICES

    @classmethod
    def get_proc_conf(cls, proc_type):
        """根据流程类型获取当前流程配置名"""
        return cls.PROCESS_TYPE_DICT[proc_type]['using']

    @classmethod
    def get_config(cls, proc_conf):
        """根据配置名获取流程配置"""
        return cls.PROCESS_CONFIG_DICT[proc_conf]['config']

    @classmethod
    def get_start_task(cls, config):
        """获取流程配置中的启动任务名"""
        return config[cls.START_TASK]

    @property
    def state_cache_key(self):
        if not hasattr(self, '_state_cache_key'):
            self._state_cache_key = self.PROCESS_STATE_CACHE % self.id
        return self._state_cache_key

    @property
    def config(self):
        if not hasattr(self, '_config'):
            self._config = self.__class__.get_config(self.proc_conf)
        return self._config

    @property
    def start_task(self):
        if not hasattr(self, '_start_task'):
            self._start_task = self.config[self.START_TASK]
        return self._start_task

    @property
    def end_task_list(self):
        if not hasattr(self, '_end_task_list'):
            self._end_task_list = self.config[self.END_TASK_LIST]
        return self._end_task_list

    @property
    def reversible_task_list(self):
        """可撤销的任务列表"""
        if not hasattr(self, '_reversible_task_list'):
            process_state_dict = self.get_process_state()
            self._reversible_task_list = [
                task_name for task_name, task_info in process_state_dict.items() if type(task_info) is dict and task_info.get('can_reverse')
            ]
        return self._reversible_task_list

    @property
    def transitable_task_list(self):
        """可执行的任务列表"""
        if not hasattr(self, '_transitable_task_list'):
            process_state_dict = self.get_process_state()
            task_list = [
                self.get_task_obj(task_name) for task_name, task_info in process_state_dict.items() if task_info.get('state') in (Task.TASK_IN_ORDER, Task.TASK_FAIL)
            ]
            self._transitable_task_list = [task_obj.name for task_obj in task_list if task_obj.is_ready()]
        return self._transitable_task_list

    def get_process_state(self):
        """获取流程的任务进度"""
        result = cache.get(self.state_cache_key)
        if result is None:
            result = json.loads(self.state_json)
            cache.set(self.state_cache_key, result, self.CACHE_TIMEOUT)
        return result

    def update_process_state(self, task_name, state_dict):
        """更新流程的任务进度"""
        process_state_dict = self.get_process_state()
        if task_name:
            process_state_dict.setdefault(task_name, {}).update(state_dict)
        else:
            process_state_dict.update(state_dict)
        # 更新memcache
        if self.ended:
            cache.delete(self.state_cache_key)
        else:
            cache.set(self.state_cache_key, process_state_dict, self.CACHE_TIMEOUT)
        # 更新数据库
        self.state_json = json.dumps(process_state_dict, cls=DjangoJSONEncoder)
        self.save()

    def get_task_obj(self, task_name):
        """根据任务名获取流程中的任务对象"""
        task_config = self.config[task_name]
        return Task(self, task_name, **task_config)

    def start(self):
        """流程开始"""
        start_task_obj = self.get_task_obj(self.start_task)
        if start_task_obj.transit_type == Task.AUTO_TRANSIT:
            return start_task_obj.transit()
        

class Task(object):
    """流程里的任务"""

    AUTO_TRANSIT = 0      # 系统自动触发运转
    MANUAL_TRANSIT = 1    # 人机交互触发运转

    TASK_FAIL = -1        # 执行失败
    TASK_IN_ORDER = 0     # 已入栈
    TASK_RUNNIG = 1       # 正在执行
    TASK_SUCCEED = 2      # 执行成功
    TASK_TRANSITED = 3    # 已出栈

    def __init__(self, process, name, name_cn, note, condition_list, run, target_list, transit_type, mutex=[]):
        self.process = process
        self.name = name
        self.name_cn = name_cn
        self.note = note
        self.transit_type = transit_type
        self.condition_list = condition_list
        self.run = run
        self.target_list = target_list
        self.mutex = mutex

    def is_ready(self):
        """判断任务的前置条件是否都已满足"""
        try:
            if self.condition_list:
                for condition in self.condition_list:
                    if callable(condition):
                        if not condition(self):
                            return False
                    elif not condition:
                        return False
            return True
        except Exception, e:
            log.error('Task condition_list error in process<%s>: %s, error: %s' % (self.process.id, self.name, e))
            return False

    def turn_in_target_list(self, org_kwargs=None):
        """转入下一步的任务列表"""
        now_ = datetime.datetime.now()
        if self.name in self.process.end_task_list:
            self.process.ended = now_
            self.process.save()
            new_state = {
                "state": self.TASK_SUCCEED,
                "updated": now_,
            }
            if org_kwargs is not None:
                new_state.update({"org_kwargs": org_kwargs})
            self.process.update_process_state(self.name, new_state)
        else:
            new_state = {
                "state": self.TASK_TRANSITED,
                "can_reverse": True,
                "updated": now_,
            }
            if org_kwargs is not None:
                new_state.update({"org_kwargs": org_kwargs})
            self.process.update_process_state(self.name, new_state)
            process_state_dict = self.process.get_process_state()
            prev_task_name = process_state_dict[self.name]['from']
            self.process.update_process_state(prev_task_name, {
                "can_reverse": False,
                "updated": now_,
            })
            for target_name in self.target_list:
                target_state = process_state_dict.get(target_name, {}).get("state", None)
                if target_state in [None, self.TASK_TRANSITED]:
                    self.process.update_process_state(target_name, {
                        "state": self.TASK_IN_ORDER,
                        "from": self.name,
                        "can_reverse": False,
                        "updated": now_,
                    })
                target = self.process.get_task_obj(target_name)
                if target.transit_type == self.AUTO_TRANSIT:
                    target.transit()

    def handle_mutex(self):
        """处理互斥任务"""
        now_ = datetime.datetime.now()
        process_state_dict = self.process.get_process_state()
        for task_name in self.mutex:
            task_state = process_state_dict.setdefault(task_name, {}).get("state", None)
            if task_state in [self.TASK_IN_ORDER, self.TASK_FAIL]:
                process_state_dict[task_name].update({
                    "state": None,
                    "updated": now_,
                })
        self.process.update_process_state(None, process_state_dict)

    def transit(self):
        """任务迁移"""
        if self.process.ended:
            return False, '该工作流程已经结束'
        process_state_dict = self.process.get_process_state()
        task_state = process_state_dict.get(self.name, {}).get("state", None)
        if task_state is None:
            log.info('The task is not in order in process<%s>: %s' % (self.process.id, self.name))
            return False, '该操作当前不可执行'
        elif task_state == self.TASK_RUNNIG:
            log.info('The task has been running in process<%s>: %s' % (self.process.id, self.name))
            return False, '该操作已在处理中'
        elif task_state == self.TASK_SUCCEED:
            self.turn_in_target_list()
            return True, '操作已完成'
        elif task_state == self.TASK_TRANSITED:
            log.info('The task was transited in process<%s>: %s' % (self.process.id, self.name))
            return False, '不能重复执行此操作'
        elif not self.is_ready():
            log.info('The task is not ready in process<%s>: %s' % (self.process.id, self.name))
            return False, '该操作尚未准备就绪'
        else:
            now_ = datetime.datetime.now()
            try:
                if callable(self.run):
                    task_state, msg, org_kwargs = self.run(self)
                else:
                    task_state, msg, org_kwargs = self.TASK_SUCCEED, '', {}

                if task_state == self.TASK_SUCCEED:
                    self.turn_in_target_list(org_kwargs)
                else:
                    self.process.update_process_state(self.name, {
                        "state": task_state,
                        "updated": now_,
                    })

                if self.mutex and task_state in [self.TASK_SUCCEED, self.TASK_RUNNIG]:
                    self.handle_mutex()

                return True, msg
            except Exception, e:
                self.process.update_process_state(self.name, {
                    "state": self.TASK_FAIL,
                    "updated": now_,
                })
                log.error('This task failed in process<%s>: %s, error: %s' % (self.process.id, self.name, e))
                return False, '发生系统错误'

    def reverse(self):
        """任务撤销"""
        if self.process.ended:
            return False, '该工作流程已经结束'
        process_state_dict = self.process.get_process_state()
        state_dict = process_state_dict.get(self.name, {})
        if state_dict['state'] != self.TASK_TRANSITED:
            return False, '该操作尚未完成，不可撤销'
        if state_dict.get('can_reverse'):
            now_ = datetime.datetime.now()
            try:
                if callable(self.run):
                    task_state, msg, org_kwargs = self.run(self, **state_dict['org_kwargs'])
                else:
                    task_state, msg, org_kwargs = self.TASK_IN_ORDER, '', {}

                if task_state == self.TASK_IN_ORDER:
                    self.turn_back()
                    # 还原互斥任务
                    if self.mutex:
                        for task_name in self.mutex:
                            task_state = process_state_dict.setdefault(task_name, {}).get("state", None)
                            if task_state is None:
                                process_state_dict[task_name].update({
                                    "state": self.TASK_IN_ORDER,
                                    "updated": now_,
                                })
                        self.process.update_process_state(None, process_state_dict)
                return True, msg
            except Exception, e:
                log.error('This task reverse failed in process<%s>: %s, error: %s' % (self.process.id, self.name, e))
                return False, '发生系统错误'

    def turn_back(self):
        """返回上级任务"""
        now_ = datetime.datetime.now()
        process_state_dict = self.process.get_process_state()
        # process_state_dict[self.name].update({
        #     "state": self.TASK_IN_ORDER,
        #     "can_reverse": False,
        #     "updated": now_,
        # })
        self.process.update_process_state(self.name, {
            "state": self.TASK_IN_ORDER,
            "can_reverse": False,
            "updated": now_,
        })
        prev_task_name = process_state_dict[self.name]['from']
        if prev_task_name:
            can_reverse = True
            prev_task = self.process.get_task_obj(prev_task_name)
            for target_name in prev_task.target_list:
                if target_name != self.name and process_state_dict.get(target_name, {}).get('state') in [self.TASK_TRANSITED, self.TASK_RUNNIG, self.TASK_SUCCEED]:
                    can_reverse = False
                    break
            if can_reverse:
                self.process.update_process_state(prev_task_name, {
                    "can_reverse": True,
                    "updated": now_,
                })
                if prev_task.transit_type == self.AUTO_TRANSIT:
                    prev_task.reverse()
