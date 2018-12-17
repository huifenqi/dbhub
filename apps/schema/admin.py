from django.contrib import admin
from django.forms import Textarea
from django.db import models
from reversion.admin import VersionAdmin

from models import Database, Table, Column, Index


class DatabaseAdmin(VersionAdmin):
    list_display = ('name', 'config', 'engine', 'charset', 'comment', 'enable')
    list_editable = ('config', 'enable')
    readonly_fields = ('engine', 'charset')


class TableAdmin(VersionAdmin):
    list_display = ('name', 'database', 'engine', 'charset', 'comment', 'is_deleted')
    search_fields = ('name', 'comment')
    readonly_fields = ('name', 'database', 'engine', 'charset')
    list_filter = ('database',)
    list_editable = ('comment',)

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 40})},
    }


class ColumnAdmin(VersionAdmin):
    list_display = ('name', 'table', 'data_type', 'is_null', 'default_value', 'comment', 'is_enum',
                    'is_comment_dirty', 'is_deleted')
    search_fields = ('name', 'table__name', 'comment')
    readonly_fields = ('name', 'table', 'data_type', 'is_null', 'default_value')
    list_filter = ('table',)
    list_editable = ('comment', 'is_enum', 'is_deleted')

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 40})},
    }


class IndexAdmin(VersionAdmin):
    list_display = ('name', 'table', 'type', 'include_columns')
    search_fields = ('name', 'table__name')
    readonly_fields = ('name', 'table', 'type', 'include_columns')


admin.site.register(Database, DatabaseAdmin)
admin.site.register(Table, TableAdmin)
admin.site.register(Column, ColumnAdmin)
admin.site.register(Index, IndexAdmin)
