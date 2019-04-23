# -*- coding: utf-8 -*-
import re


class CommentParser(object):
    @classmethod
    def parse(cls, comment):
        pattern = r"([-\d\w]+)([:|：|-]{1})\s*[^:：,，-]?"
        objs = re.findall(pattern, comment, re.M | re.I)
        return objs

    @classmethod
    def parse_with_lark(cls, comment):
        from lark import Lark
        parser = Lark('''start: WORD "," WORD "!"
                    LCASE_LETTER: "a".."z"
                    UCASE_LETTER: "A".."Z"
                    CN_ZH_LETTER: /[u"\u4e00-\u9fa5"]/
                    LETTER: UCASE_LETTER | LCASE_LETTER | CN_ZH_LETTER
                    WORD: LETTER+
                    %import common.NUMBER   // imports from terminal library
                    %ignore " "           // Disregard spaces in text
                 ''', parser='lalr')

        print(parser.parse(comment).pretty())
        # print(parser.parse(u'默认代扣银行卡 1:默认代扣 0:不默认代扣'))
        # not works as parsing library need accurate sentence

    @classmethod
    def get_enums(cls, comment):
        enums = list(set([obj[0] for obj in cls.parse(comment)]))
        return sorted(enums)


def run(db_list, t_list):
    from xlibs.db import DB
    from apps.schema.models import Database
    db_name_list = db_list.split(',')
    if len(db_name_list) == 1 and db_name_list[0] == '':
        databases = Database.objects.filter(enable=True)
    else:
        databases = Database.objects.filter(enable=True, name__in=db_name_list)
    for database in databases:
        t_name_list = t_list.split(',')
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
                comment_enums = CommentParser.get_enums(column.comment or '')
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
                enum_list = tb.group_by(column.name).all()
                if len(enum_list) > 50:
                    print '枚举值可能异常', database, table, column
                    continue
                real_enums = [str(getattr(row, column.name)) for row in enum_list]
                no_match_enums = (set(real_enums) - set(comment_enums))
                if no_match_enums:
                    print database, table, column, comment_enums, real_enums
                    column.is_comment_dirty = True
                    warning = ','.join(no_match_enums)
                    column.other_enums = warning
                column.save()

