# -*- coding: utf-8 -*-
import pymongo

from apps.schema.models import Database
from scripts.db import DB
from scripts.parser import CommentParser


class Checker(object):
    def __init__(self, database, t_name_list):
        self.database = database
        self.dialect = database.config.split(':')[0]
        if self.dialect == 'mongodb':
            parts1 = self.database.config.rsplit(':', 1)
            parts2 = parts1[1].split('/')
            host = parts1[0]
            port = int(parts2[0])
            db_name = parts2[1]
            self.db = pymongo.MongoClient(host, port)[db_name]
        else:
            self.db = DB(self.database.config)
        if len(t_name_list) == 1 and t_name_list[0] == '':
            tables = database.table_set.all()
        else:
            tables = database.table_set.filter(name__in=t_name_list)
            if not tables:
                tables = database.table_set.all()
        self.tables = tables

    def get_enum_list(self, table_name, column_name):
        real_enums = []
        if self.dialect == 'mongodb':
            pipeline = [
                {
                    u"$group": {
                        u"_id": {
                            column_name: u"${}".format(column_name)
                        },
                        u"COUNT(*)": {
                            u"$sum": 1
                        }
                    }
                },
                {
                    u"$project": {
                        column_name: u"$_id.{}".format(column_name),
                        u"COUNT(*)": u"$COUNT(*)",
                        u"_id": 0
                    }
                }
            ]
            cursor = self.db[table_name].aggregate(pipeline, allowDiskUse=True)
            real_enums = [r[column_name] for r in cursor]
        else:
            tb = getattr(self.db, table_name)
            enum_list = tb.group_by(column_name).all()
            for row in enum_list:
                tmp = getattr(row, column_name)
                if isinstance(tmp, unicode):
                    real_enums.append(tmp.encode('utf-8'))
                else:
                    real_enums.append(str(tmp))
        return real_enums

    def run(self):
        for table in self.tables:
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
                real_enums = self.get_enum_list(table.name, column.name)
                if len(real_enums) > 50:
                    column.other_enums = u'枚举值异常!'
                    column.is_comment_dirty = True
                    column.save()
                    continue
                not_match_enums = (set(real_enums) - set(comment_enums))
                if not_match_enums:
                    print(self.database, table, column, comment_enums, real_enums)
                    column.is_comment_dirty = True
                    warning = ','.join(not_match_enums)
                    column.other_enums = warning
                else:
                    column.is_comment_dirty = False
                column.save()


def run(db_list, t_list):
    db_name_list = db_list.split(',')
    if len(db_name_list) == 1 and db_name_list[0] == '':
        databases = Database.objects.filter(enable=True)
    else:
        databases = Database.objects.filter(enable=True, name__in=db_name_list)
    t_name_list = t_list.split(',')
    for database in databases:
        checker = Checker(database, t_name_list)
        checker.run()
