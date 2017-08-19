# -*- coding:utf-8 -*-

from torcms.modules.modef import core_modules


def Test():
    assert type(core_modules) == type(dict())
