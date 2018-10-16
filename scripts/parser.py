# -*- coding: utf-8 -*-
import re

from xlibs.db import DB
from apps.schema.models import Database


class CommentParser(object):
    @classmethod
    def parse(cls, comment):
        pattern = r"(\d+)[:|：|,|，|-]\s*([^\x00-\xff]+)"
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
        enums = [obj[0] for obj in cls.parse(comment)]
        return sorted(enums)


def test():
    cp = CommentParser()
    # cp.parse_with_lark(u'默认代扣银行卡 1:默认代扣 0:不默认代扣')
    t = u"""
        是否启用
        0: 启用
        1: 停用
        """
    objs = cp.get_enums(t)
    print objs
    t = u'默认代扣银行卡 1:默认代扣 0:不默认代扣'
    objs = cp.get_enums(t)
    print objs
    t = u'是否在线，0-离线 1-在线'
    objs = cp.get_enums(t)
    print objs


def run():
    cp = CommentParser()
    databases = Database.objects.filter(enable=True)
    for database in databases:
        db = DB(database.config)
        for table in database.table_set.all():
            for column in table.column_set.filter(is_enum=True):
                comment_enums = cp.get_enums(column.comment)
                tb = getattr(db, table.name)
                real_enums = [getattr(row, column.name) for row in tb.group_by(column.name).all()]
                if set(real_enums) - set(comment_enums):
                    print database, table, column, 'comment dirty'
                    column.is_comment_dirty = True
                    column.save()


if __name__ == '__main__':
    test()
