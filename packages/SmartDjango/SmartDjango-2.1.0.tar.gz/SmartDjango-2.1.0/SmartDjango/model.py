import datetime
from typing import Tuple, List

from django.db import models
from django.db.models import Q

from .attribute import Attribute
from .error import BaseError
from .packing import Packing


class Constraint:
    def __init__(self, field, _type, boundary=True, compare=None, template=None, max_min_fit=None):
        self.field = field
        self.type = _type
        self.boundary = boundary
        self.compare = compare or (lambda x: x)
        self.error_template = template or '{0} should %s than {1}'
        self.max_min_fit = max_min_fit or ('less', 'more')


CONSTRAINTS = [
    Constraint(
        models.CharField, str,
        template='{0}长度不应%s{1}字符',
        compare=lambda x: len(x),
        max_min_fit=('超过', '少于')
    ),
    Constraint(
        models.IntegerField, int,
        template='{0}不应%s{1}',
        max_min_fit=('大于', '小于')
    ),
    Constraint(models.DateTimeField, datetime.datetime, boundary=False),
    Constraint(models.DateField, datetime.date, boundary=False),
    Constraint(models.BooleanField, bool, boundary=False),
]


class SmartQuerySet(models.QuerySet):
    def search(self, *args, **kwargs):
        objects = self.all()
        cls = self.model

        field_dict = dict()
        for o_field in cls._meta.fields:
            field_dict[o_field.name] = o_field

        for q in args:
            if isinstance(q, Q):
                objects = objects.filter(q)

        for attr in kwargs:
            attr_value = kwargs[attr]

            if attr.endswith('__null'):
                attr = attr[:-6]
            elif attr_value is None:
                continue

            full = attr.endswith('__full')
            if full:
                attr = attr[:-6]

            filter_func = getattr(cls, '_search_%s' % attr, None)
            if filter_func and callable(filter_func):
                o_filter = filter_func(attr_value)
                if isinstance(o_filter, dict):
                    objects = objects.filter(**o_filter)
                elif isinstance(o_filter, Q):
                    objects = objects.filter(o_filter)
                continue

            if attr in field_dict:
                attr_field = field_dict[attr]
            else:
                attr_field = None

            filter_dict = dict()
            if not full and \
                    (isinstance(attr_field, models.CharField) or
                     isinstance(attr_field, models.TextField)):
                filter_dict.setdefault('%s__contains' % attr, attr_value)
            else:
                filter_dict.setdefault(attr, attr_value)

            objects = objects.filter(**filter_dict)
        return objects

    def dict(self, dictor):
        if callable(dictor):
            return list(map(dictor, self))
        return self

    def page(self, pager, last=0, count=5):
        return pager.page(self, last=last, count=count)


class SmartManager(models.Manager):
    def __init__(self):
        super().__init__()
        self.restrict_args = tuple()
        self.restrict_kwargs = dict()

    def get_queryset(self):
        return SmartQuerySet(self.model, using=self._db).filter(*self.restrict_args,
                                                                **self.restrict_kwargs)

    def restrict(self, *args, **kwargs):
        self.restrict_args = args
        self.restrict_kwargs = kwargs
        return self

    def search(self, *args, **kwargs):
        return self.all().search(*args, **kwargs)

    def dict(self, dictor):
        return self.all().dict(dictor)

    def page(self, pager, last=0, count=5):
        return pager.page(self.all(), last=last, count=count)


class SmartModel(models.Model):
    objects = SmartManager()

    class Meta:
        abstract = True

    @classmethod
    def get_fields(cls, field_names: List[str]) -> Tuple[models.Field]:
        field_dict = {}
        for field in cls._meta.fields:
            field_dict[field.name] = field

        fields = []  # type: List[models.Field]
        for field_name in field_names:
            fields.append(field_dict.get(field_name))

        return tuple(fields)

    @classmethod
    def get_field(cls, field_name):
        return cls.get_fields([field_name])[0]

    @classmethod
    def get_params(cls, field_names):
        from .param import Param
        return Param.from_fields(cls.get_fields(field_names))

    @classmethod
    def get_param(cls, field_name):
        from .param import Param
        return Param.from_field(cls.get_field(field_name))

    F = get_fields
    P = get_params

    @staticmethod
    def d_self(self):
        return self

    @classmethod
    def field_validator(cls, field):
        attr = field.name
        verbose = field.verbose_name
        cls_ = field.model

        @Packing.pack
        def _validator(value):
            for constraint in CONSTRAINTS:
                if isinstance(field, constraint.field):
                    if not isinstance(value, constraint.type):
                        return BaseError.FIELD_FORMAT('%s(%s)类型错误' % (attr, verbose))
                    if constraint.boundary:
                        max_l = getattr(cls_, 'MAX_L', None)
                        if max_l and attr in max_l and max_l[attr] < constraint.compare(value):
                            return BaseError.FIELD_FORMAT(
                                (constraint.error_template % constraint.max_min_fit[0]).format(
                                    verbose, max_l[attr]))
                        min_l = getattr(cls_, 'MIN_L', None)
                        if min_l and attr in min_l and constraint.compare(value) < min_l[attr]:
                            return BaseError.FIELD_FORMAT(
                                (constraint.error_template % constraint.max_min_fit[1]).format(
                                    verbose, min_l[attr]))
                    break

            if field.choices:
                choice_match = False
                for choice in field.choices:
                    if value == choice[0]:
                        choice_match = True
                        break
                if not choice_match:
                    return BaseError.FIELD_FORMAT('%s(%s)不在可选择范围之内' % (attr, verbose))

            return value
        return _validator

    @classmethod
    @Packing.pack
    def validator(cls, attr_dict):
        if not isinstance(attr_dict, dict):
            return BaseError.FIELD_VALIDATOR
        if not isinstance(cls(), SmartModel):
            return BaseError.FIELD_VALIDATOR

        # 获取字段字典
        field_dict = dict()
        for o_field in cls._meta.fields:
            field_dict[o_field.name] = o_field

        # 遍历传入的参数
        for attr in attr_dict:
            attr_value = attr_dict[attr]
            if attr in field_dict:
                # 参数名为字段名
                attr_field = field_dict[attr]
            else:
                attr_field = None

            if isinstance(attr_field, models.Field):
                if attr_field.null and attr_value is None:
                    return
                if not attr_field.null and attr_value is None:
                    return BaseError.FIELD_FORMAT(
                        '%s(%s)不允许为空' % (attr_field.name, attr_field.verbose_name))
                ret = cls.field_validator(attr_field)(attr_value)
                if not ret.ok:
                    return ret

            # custom validation functions
            valid_func = getattr(cls, '_valid_%s' % attr, None)
            if valid_func and callable(valid_func):
                try:
                    ret = valid_func(attr_value)
                    if not ret.ok:
                        return ret
                except Exception:
                    return BaseError.FIELD_VALIDATOR(
                        '%s校验函数崩溃',
                        attr_field.verbose_name if isinstance(attr_field, models.Field) else attr)

    def dictor(self, field_list):
        return Attribute.dictor(self, field_list)
