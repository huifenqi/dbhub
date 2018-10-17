# -*- coding: utf-8 -*-
import re

from xlibs.db import DB


class CommentParser(object):
    @classmethod
    def parse(cls, comment):
        pattern = r"([-\d\w]+)([:|：|,|，|-]{1})\s*[^:：,，-]?"
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


def run():
    from apps.schema.models import Database
    databases = Database.objects.filter(enable=True)
    for database in databases:
        db = DB(database.config)
        for table in database.table_set.all():
            for column in table.column_set.all():
                # skip column which is dirty
                if column.is_comment_dirty:
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
                real_enums = [getattr(row, column.name) for row in tb.group_by(column.name).all()]
                if set(real_enums) - set(comment_enums):
                    print database, table, column, comment_enums, real_enums
                    column.is_comment_dirty = True
                column.save()
