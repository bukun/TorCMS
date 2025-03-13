# -*- coding:utf-8 -*-

from torcms.modules.modef import core_modules


def test_foo():
    assert type(core_modules) == type({})
