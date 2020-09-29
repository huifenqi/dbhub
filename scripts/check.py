# -*- coding: utf-8 -*-

from apps.schema.models import Database
from scripts.db import DB
from scripts.parser import CommentParser


def run(db_list, t_list):
    db_name_list = db_list.split(',')
    if len(db_name_list) == 1 and db_name_list[0] == '':
        databases = Database.objects.filter(enable=True)
    else:
        databases = Database.objects.filter(enable=True, name__in=db_name_list)
    t_name_list = t_list.split(',')
    for database in databases:
        if database.config.startswith('mongodb'):
            continue
        if len(t_name_list) == 1 and t_name_list[0] == '':
            tables = database.table_set.all()
        else:
            tables = database.table_set.filter(name__in=t_name_list)
            if not tables:
                tables = database.table_set.all()
        db = DB(database.config)
        for table in tables:
            for column in table.column_set.all():
                # skip column which is dirty
                if column.is_comment_dirty or column.is_deleted:
                    continue
                comment_enums = CommentParser.get_enums((column.comment or '').encode('utf-8'))
                # set is_enum as have comment_enums
                if comment_enums and not column.is_enum:
                    column.is_enum = True
                # skip column which is not enum
                if not column.is_enum:
                    continue
                try:
                    tb = getattr(db, table.name)
                except Exception:
                    continue
                enum_count = tb.group_by(column.name).count()
                if enum_count > 50:
                    column.other_enums = u'枚举值异常!'
                    column.is_comment_dirty = True
                    column.save()
                    continue
                real_enums = []
                enum_list = tb.group_by(column.name).all()
                for row in enum_list:
                    tmp = getattr(row, column.name)
                    if isinstance(tmp, unicode):
                        real_enums.append(tmp.encode('utf-8'))
                    else:
                        real_enums.append(str(tmp))
                no_match_enums = (set(real_enums) - set(comment_enums))
                if no_match_enums:
                    print(database, table, column, comment_enums, real_enums)
                    column.is_comment_dirty = True
                    warning = ','.join(no_match_enums)
                    column.other_enums = warning
                else:
                    column.is_comment_dirty = False
                column.save()
