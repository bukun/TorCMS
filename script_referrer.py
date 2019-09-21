# -*- coding:utf-8 -*-

# 创建 访问来源 记录表 Tabreferrer
from torcms.model.referrer_model import *

try:
    Tabreferrer.create_table()
except:
    pass
