# coding: utf-8
from __future__ import unicode_literals

import django_tables2 as tables

from models import Column


TEMPLATE = """
{% if record.is_deleted %}<span class="ui red label">Deleted</span>{% endif %}
{% if record.is_comment_dirty %}<span class="ui yellow label">Not Match</span>{% endif %}
"""


class ColumnTable(tables.Table):
    table_comment = tables.TemplateColumn('{{ value|linebreaks }}', verbose_name='Table Comment',
                                          accessor='table.comment')
    comment = tables.TemplateColumn('{{ value|linebreaks }}')
    warning_info = tables.TemplateColumn(TEMPLATE, verbose_name='Warning', orderable=False)

    class Meta:
        model = Column
        sequence = ('name', 'table', 'data_type', 'is_null', 'default_value', 'comment', 'table_comment',
                    'warning_info')
        template_name = "django_tables2/semantic.html"
        exclude = ("id", "is_comment_dirty", "is_enum", "is_deleted")
