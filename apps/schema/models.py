# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models


class Database(models.Model):
    name = models.CharField(unique=True, max_length=100, help_text=u'数据库名')
    config = models.CharField(max_length=1000, help_text=u'配置')
    engine = models.CharField(max_length=10, help_text=u'引擎', null=True, blank=True)
    charset = models.CharField(max_length=100, help_text=u'编码', null=True, blank=True)
    comment = models.CharField(max_length=5000, help_text=u'注释', null=True, blank=True)


class Table(models.Model):
    database = models.ForeignKey(Database)
    name = models.CharField(max_length=100, help_text=u'表名')
    comment = models.CharField(max_length=5000, help_text=u'注释', null=True, blank=True)


class Column(models.Model):
    NULL_TYPES = (
        (True, 'NULL'),
        (False, 'NOT NULL'),
    )

    table = models.ForeignKey(Table)
    name = models.CharField(max_length=100, help_text=u'列名')
    data_type = models.CharField(max_length=100, help_text=u'数据类型')
    is_null = models.BooleanField(choices=NULL_TYPES, help_text=u'可空')
    default_value = models.CharField(max_length=1000, help_text=u'默认值', null=True, blank=True)
    comment = models.CharField(max_length=5000, help_text=u'注释', null=True, blank=True)


class Index(models.Model):
    table = models.ForeignKey(Table)
    name = models.CharField(max_length=100, help_text=u'索引名')
    type = models.CharField(max_length=100, help_text=u'类型')
    include_columns = models.CharField(max_length=1000, help_text=u'包含字段', null=True, blank=True)
