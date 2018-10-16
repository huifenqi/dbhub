from django.contrib import admin
from django.forms import Textarea
from django.db import models

from models import Database, Table, Column, Index


class DatabaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'config', 'engine', 'charset', 'comment', 'enable')
    list_editable = ('config', 'enable')
    readonly_fields = ('engine', 'charset')


class TableAdmin(admin.ModelAdmin):
    list_display = ('name', 'database', 'engine', 'charset', 'comment')
    search_fields = ('name', 'comment')
    readonly_fields = ('name', 'database', 'engine', 'charset')
    list_filter = ('database',)
    list_editable = ('comment',)

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 40})},
    }


class ColumnAdmin(admin.ModelAdmin):
    @staticmethod
    def table_database(obj):
        return '{} ({})'.format(obj.table.name, obj.table.database.name)

    list_display = ('name', 'table_database', 'data_type', 'is_null', 'default_value', 'comment', 'is_enum',
                    'is_deleted')
    search_fields = ('name', 'table__name', 'comment')
    readonly_fields = ('name', 'table', 'data_type', 'is_null', 'default_value')
    list_filter = ('table',)
    list_editable = ('comment', 'is_enum', 'is_deleted')

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 40})},
    }


class IndexAdmin(admin.ModelAdmin):
    @staticmethod
    def database_name(obj):
        return obj.table.database.name

    list_display = ('name', 'table', 'database_name', 'type', 'include_columns')
    search_fields = ('name', 'table__name')
    readonly_fields = ('name', 'table', 'database_name', 'type', 'include_columns')


admin.site.register(Database, DatabaseAdmin)
admin.site.register(Table, TableAdmin)
admin.site.register(Column, ColumnAdmin)
admin.site.register(Index, IndexAdmin)
