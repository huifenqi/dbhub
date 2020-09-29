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
