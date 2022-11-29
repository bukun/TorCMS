# coding:utf-8

from pathlib import Path
from torcms.modules.modef import core_modules

CUR_MODUES = core_modules  # type: Dict[str, object]

for wdir in Path('.').iterdir():
    if wdir.is_dir() and wdir.name.startswith('torcms_'):
        the_file = f'{wdir.name}.modules.modef'
        print(the_file)
        d = __import__(the_file)

        CUR_MODUES = dict(CUR_MODUES, **d.modules.modef._modules)

_CUR_MODUES = CUR_MODUES
