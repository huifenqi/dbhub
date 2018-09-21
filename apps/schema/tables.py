# coding: utf-8
from __future__ import unicode_literals

import django_tables2 as tables

from models import Column


class ColumnTable(tables.Table):
    table_comment = tables.TemplateColumn('{{ value|linebreaks }}', verbose_name='Table Comment',
                                          accessor='table.comment')
    comment = tables.TemplateColumn('{{ value|linebreaks }}')

    class Meta:
        model = Column
        sequence = ('name', 'table', 'data_type', 'is_null', 'default_value', 'comment', 'table_comment')
        template_name = "django_tables2/semantic.html"
        exclude = ("id",)
