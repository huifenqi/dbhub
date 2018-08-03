from django.contrib import admin

from models import Database, Table, Column, Index


class DatabaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'config', 'engine', 'charset', 'comment')


class TableAdmin(admin.ModelAdmin):
    list_display = ('name', 'database', 'engine', 'charset', 'comment')


class ColumnAdmin(admin.ModelAdmin):
    list_display = ('name', 'table', 'data_type', 'is_null', 'default_value', 'comment')


class IndexAdmin(admin.ModelAdmin):
    list_display = ('name', 'table', 'type', 'include_columns')


admin.site.register(Database, DatabaseAdmin)
admin.site.register(Table, TableAdmin)
admin.site.register(Column, ColumnAdmin)
admin.site.register(Index, IndexAdmin)
