from django.contrib import admin

from models import Database, Table, Column, Index


class DatabaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'config', 'engine', 'charset', 'comment', 'enable')
    list_editable = ('config', 'enable')


class TableAdmin(admin.ModelAdmin):
    list_display = ('name', 'database', 'engine', 'charset', 'comment')


class ColumnAdmin(admin.ModelAdmin):
    @staticmethod
    def table_database(obj):
        return '{} ({})'.format(obj.table.name, obj.table.database.name)

    list_display = ('name', 'table_database', 'data_type', 'is_null', 'default_value', 'comment')
    search_fields = ('name', 'table__name', 'comment')


class IndexAdmin(admin.ModelAdmin):
    @staticmethod
    def database_name(obj):
        return obj.table.database.name

    list_display = ('name', 'table', 'database_name', 'type', 'include_columns')
    search_fields = ('name', 'table__name')


admin.site.register(Database, DatabaseAdmin)
admin.site.register(Table, TableAdmin)
admin.site.register(Column, ColumnAdmin)
admin.site.register(Index, IndexAdmin)
