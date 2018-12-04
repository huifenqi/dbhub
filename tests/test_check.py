# -*- coding: utf-8 -*-
import pytest

from scripts.check import CommentParser


@pytest.mark.parametrize('comment, expected', [
    (u"""
        是否启用
        0: 启用
        1: 停用
        """, [u'0', u'1']),
    (u'默认代扣银行卡 1:默认代扣 0:不默认代扣', [u'0', u'1']),
    (u'是否在线，0-离线 1-在线', [u'0', u'1']),
    (u"""1:xxx
        2:zzz""", [u'1', u'2']),
    (u"""银行账户开户行 PABC:平安银行 SPDB:浦发银行 HXB:华夏银行...参考程序枚举""", [u'HXB', u'PABC', u'SPDB']),
    # (u'xxx', 'xxx'),
    (u"""扣款状态,-1-未发起,0-已发起,1-扣款成功,2-扣款失败,3-处理中,4-不一致""", [u'-1', u'0', u'1', u'2', u'3', u'4']),
    (u'前置电签状态：-1-调用北银接口程序异常；0：成功，1：失败；系统异常则返回系统错误码', [u'-1']),
    (u'门店是否启用:0:否,1:是', [u'0', u'1']),
    (u"""
charset with description, blah, blah, blah

utf8: A UTF-8 encoding of the Unicode character set using one to three bytes per character. default utf8 of mysql, max length is 3 bytes, not support characters, such as emoji.

utf8mb4: A UTF-8 encoding of the Unicode character set using one to four bytes per character.
    """, ['UTF', u'utf8', u'utf8mb4']), # error case
])
def test_get_enums(comment, expected):
    real = CommentParser.get_enums(comment)
    assert expected == real
