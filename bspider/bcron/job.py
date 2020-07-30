from inspect import ismethod, isclass
from datetime import datetime

import six
from apscheduler.job import Job
from apscheduler.triggers.base import BaseTrigger
from apscheduler.util import convert_to_datetime, ref_to_obj, obj_to_ref, get_callable_name, check_callable_args
try:
    from collections.abc import Iterable, Mapping
except ImportError:
    from collections import Iterable, Mapping


class MySQLJob(Job):

    def __init__(self, scheduler, id=None, **kwargs):
        self._scheduler = scheduler
        self._jobstore_alias = None
        self._modify(id=id, **kwargs)

    def _modify(self, **changes):
        """
        Validates the changes to the Job and makes the modifications if and only if all of them
        validate.

        """
        approved = {}

        if 'id' in changes:
            value = changes.pop('id')
            if not isinstance(value, int):
                raise TypeError("id must be a int")
            approved['id'] = value

        if 'func' in changes or 'args' in changes or 'kwargs' in changes:
            func = changes.pop('func') if 'func' in changes else self.func
            args = changes.pop('args') if 'args' in changes else self.args
            kwargs = changes.pop(
                'kwargs') if 'kwargs' in changes else self.kwargs

            if isinstance(func, six.string_types):
                func_ref = func
                func = ref_to_obj(func)
            elif callable(func):
                try:
                    func_ref = obj_to_ref(func)
                except ValueError:
                    # If this happens, this Job won't be serializable
                    func_ref = None
            else:
                raise TypeError(
                    'func must be a callable or a textual reference to one')

            if not hasattr(self, 'name') and changes.get('name', None) is None:
                changes['name'] = get_callable_name(func)

            if isinstance(args, six.string_types) or not isinstance(args, Iterable):
                raise TypeError('args must be a non-string iterable')
            if isinstance(kwargs, six.string_types) or not isinstance(kwargs, Mapping):
                raise TypeError('kwargs must be a dict-like object')

            check_callable_args(func, args, kwargs)

            approved['func'] = func
            approved['func_ref'] = func_ref
            approved['args'] = args
            approved['kwargs'] = kwargs

        if 'name' in changes:
            value = changes.pop('name')
            if not value or not isinstance(value, six.string_types):
                raise TypeError("name must be a nonempty string")
            approved['name'] = value

        if 'misfire_grace_time' in changes:
            value = changes.pop('misfire_grace_time')
            if value is not None and (not isinstance(value, six.integer_types) or value <= 0):
                raise TypeError(
                    'misfire_grace_time must be either None or a positive integer')
            approved['misfire_grace_time'] = value

        if 'coalesce' in changes:
            value = bool(changes.pop('coalesce'))
            approved['coalesce'] = value

        if 'max_instances' in changes:
            value = changes.pop('max_instances')
            if not isinstance(value, six.integer_types) or value <= 0:
                raise TypeError('max_instances must be a positive integer')
            approved['max_instances'] = value

        if 'trigger' in changes:
            # 暂时先这样，后续支持多种定时任务的时候再进行修改
            trigger = changes.pop('trigger')
            if not isinstance(trigger, BaseTrigger):
                raise TypeError('Expected a trigger instance, got %s instead' %
                                trigger.__class__.__name__)

            # 每次更新trigger就重新计算下次执行时间
            now = datetime.now(self._scheduler.timezone)
            changes['next_run_time'] = trigger.get_next_fire_time(None, now)

            approved['trigger'] = trigger

        if 'executor' in changes:
            value = changes.pop('executor')
            if not isinstance(value, six.string_types):
                raise TypeError('executor must be a string')
            approved['executor'] = value

        if 'next_run_time' in changes:
            value = changes.pop('next_run_time')
            approved['next_run_time'] = convert_to_datetime(value, self._scheduler.timezone,
                                                            'next_run_time')
        # 新增两个属性 status, description
        if 'status' in changes:
            value = changes.pop('status')
            if value not in [0, 1]:
                raise TypeError("name status be 0 (closed) or 1(open)")
            approved['status'] = value

        if 'description' in changes:
            value = changes.pop('description')
            if not value or not isinstance(value, six.string_types):
                raise TypeError("description must be a nonempty string")
            approved['description'] = value

        if 'cron_type' in changes:
            value = changes.pop('cron_type')
            if not value or value not in ('operation', 'crawl'):
                raise TypeError("cron type must be operation or crawl")
            approved['type'] = value

        if changes:
            raise AttributeError('The following are not modifiable attributes of Job: %s' %
                                 ', '.join(changes))

        for key, value in six.iteritems(approved):
            setattr(self, key, value)

    def __getstate__(self):
        # Don't allow this Job to be serialized if the function reference could not be determined
        if not self.func_ref:
            raise ValueError(
                'This Job cannot be serialized since the reference to its callable (%r) could not '
                'be determined. Consider giving a textual reference (module:function name) '
                'instead.' % (self.func,))

        # Instance methods cannot survive serialization as-is, so store the "self" argument
        # explicitly
        if ismethod(self.func) and not isclass(self.func.__self__):
            args = (self.func.__self__,) + tuple(self.args)
        else:
            args = self.args

        return {
            'version': 1,
            'id': self.id,
            'func': self.func_ref,
            'trigger': self.trigger,
            'executor': self.executor,
            'args': args,
            'kwargs': self.kwargs,
            'name': self.name,
            'misfire_grace_time': self.misfire_grace_time,
            'coalesce': self.coalesce,
            'max_instances': self.max_instances,
            'next_run_time': self.next_run_time,
            # 新增两个属性 status, description
            'status': self.status,
            'description': self.description,
            # 新增属性type
            'type': self.cron_type
        }

    def __setstate__(self, state):
        if state.get('version', 1) > 1:
            raise ValueError('Job has version %s, but only version 1 can be handled' %
                             state['version'])

        self.id = state['id']
        self.func_ref = state['func']
        self.func = ref_to_obj(self.func_ref)
        self.trigger = state['trigger']
        self.executor = state['executor']
        self.args = state['args']
        self.kwargs = state['kwargs']
        self.name = state['name']
        self.misfire_grace_time = state['misfire_grace_time']
        self.coalesce = state['coalesce']
        self.max_instances = state['max_instances']
        self.next_run_time = state['next_run_time']
        # 新增两个属性 status, description
        self.status = state['status']
        self.description = state['description']
        # 新增属性type
        self.cron_type = state['type']

    def __repr__(self):
        return '<MySQLJob (id=%s name=%s)>' % (self.id, self.name)
