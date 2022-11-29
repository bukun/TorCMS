# -*- coding:utf-8 -*-

import peewee
from playhouse.postgres_ext import BinaryJSONField
from torcms.core.base_model import BaseModel


class ExtabCalcInfo(BaseModel):
    uid = peewee.CharField(null=False, index=True, unique=True, primary_key=True, max_length=36, help_text='', )
    title = peewee.CharField(null=False, help_text='标题', )
    post_id = peewee.CharField(null=False, max_length=5, help_text='', )
    user_id = peewee.CharField(null=False, max_length=36, help_text='', )
    time_create = peewee.IntegerField(default=0, null=False)
    time_update = peewee.IntegerField(default=0, null=False)
    extinfo = BinaryJSONField()
