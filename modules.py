# coding:utf-8

from pathlib import Path
from torcms.modules.modef import core_modules
from config import config_modules

CUR_MODUES = dict(core_modules, **config_modules)  # type: Dict[str, object]

for wdir in Path('.').iterdir():
    if wdir.is_dir() and wdir.name.startswith('torcms_'):
        the_file = f'{wdir.name}.modules.modef'
        _mod = __import__(the_file)

        CUR_MODUES = dict(CUR_MODUES, **_mod.modules.modef._modules)

_CUR_MODUES = CUR_MODUES
