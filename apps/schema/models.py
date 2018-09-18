# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models


class Database(models.Model):
    NULL_TYPES = (
        (True, 'on'),
        (False, 'off'),
    )
    name = models.CharField(unique=True, max_length=100, help_text=u'数据库名')
    config = models.URLField(unique=True, max_length=1000, help_text=u'配置')
    engine = models.CharField(max_length=10, help_text=u'引擎', default='InnoDB', null=True, blank=True)
    charset = models.CharField(max_length=100, help_text=u'编码', default='utf8', null=True, blank=True)
    comment = models.TextField(max_length=5000, help_text=u'注释', default='TBD', null=True, blank=True)
    enable = models.NullBooleanField(choices=NULL_TYPES, help_text=u'是否启用', default=False, null=True, blank=True)

    def __unicode__(self):
        return self.name


class Table(models.Model):
    database = models.ForeignKey(Database)
    name = models.CharField(max_length=100, help_text=u'表名')
    engine = models.CharField(max_length=10, help_text=u'引擎', null=True, blank=True)
    charset = models.CharField(max_length=100, help_text=u'编码', null=True, blank=True)
    comment = models.TextField(max_length=5000, help_text=u'注释', null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = (('database', 'name'),)


class Column(models.Model):
    NULL_TYPES = (
        (True, 'NULL'),
        (False, 'NOT NULL'),
    )

    table = models.ForeignKey(Table)
    name = models.CharField(max_length=100, help_text=u'列名')
    data_type = models.CharField(max_length=100, help_text=u'数据类型', null=True, blank=True)
    is_null = models.NullBooleanField(choices=NULL_TYPES, help_text=u'可空', null=True, blank=True)
    default_value = models.CharField(max_length=1000, help_text=u'默认值', null=True, blank=True)
    comment = models.TextField(max_length=5000, help_text=u'注释', null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = (('table', 'name'),)


class Index(models.Model):
    KEY_TYPES = (
        ('KEY', 'KEY'),
        ('PRIMARY KEY', 'PRIMARY KEY'),
        ('UNIQUE KEY', 'UNIQUE KEY'),
    )

    table = models.ForeignKey(Table)
    name = models.CharField(max_length=100, help_text=u'索引名')
    type = models.CharField(max_length=100, choices=KEY_TYPES, help_text=u'类型', null=True, blank=True)
    include_columns = models.CharField(max_length=1000, help_text=u'包含字段', null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = (('table', 'name'),)
