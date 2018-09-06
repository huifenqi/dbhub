# -*- coding: utf-8 -*-
import re
from lark import Lark


def parse(comment):
    pattern = r"(\d+)[:|：|,|，]([^\x00-\xff]+)"
    objs = re.findall(pattern, comment, re.M | re.I)
    return objs


def parse_chinese():
    parser = Lark('''start: WORD "," WORD "!"
                LCASE_LETTER: "a".."z"
                UCASE_LETTER: "A".."Z"
                CN_ZH_LETTER: /[u"\u4e00-\u9fa5"]/
                LETTER: UCASE_LETTER | LCASE_LETTER | CN_ZH_LETTER
                WORD: LETTER+
                %import common.NUMBER   // imports from terminal library
                %ignore " "           // Disregard spaces in text
             ''', parser='lalr')

    print(parser.parse(u"Hello,世界!").pretty())
    # print(parser.parse(u'默认代扣银行卡 1:默认代扣 0:不默认代扣'))
    # not works as parsing library need accurate sentence


if __name__ == '__main__':
    parse_chinese()
    objs = parse(u'默认代扣银行卡 1:默认代扣 0:不默认代扣')
    for obj in objs:
        print obj
