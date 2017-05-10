# -*- coding:utf-8 -*-

'''
Used for Map.
'''

import peewee
from playhouse.postgres_ext import JSONField
from torcms.core.base_model import BaseModel


class MabGson(BaseModel):
    '''
    For GeoJson storage.
    '''
    uid = peewee.CharField(null=False, index=True,
                           unique=True, primary_key=True, max_length=4, help_text='', )
    title = peewee.CharField(null=False, default='')
    user_id = peewee.CharField(null=False, index=True, max_length=36, help_text='', )
    json = JSONField()
    time_create = peewee.IntegerField(null=False, default=0)
    time_update = peewee.IntegerField(null=False, default=0)
    public = peewee.IntegerField(null=False, default=0)


class MabPost2Gson(BaseModel):
    '''
    relatio between Post2Json.
    '''
    uid = peewee.CharField(null=False, index=True, unique=True,
                           primary_key=True, max_length=36, help_text='')
    post_id = peewee.CharField(null=False, index=True, max_length=5, help_text='', )
    json_id = peewee.CharField(null=False, index=True, max_length=4, help_text='', )

class MabLayout(BaseModel):
    '''
    For Map layout.
    '''
    uid = peewee.CharField(null=False, index=True, unique=True,
                           primary_key=True, max_length=8, help_text='', )
    title = peewee.CharField(null=False, default='')
    post_id = peewee.CharField(null=False, index=True, max_length=5, help_text='', )
    user_id = peewee.CharField(null=False, index=True, max_length=36, help_text='', )
    json = peewee.CharField(null=True, default='', max_length=4)
    lon = peewee.FloatField(null=False, default=105)
    lat = peewee.FloatField(null=False, default=36)
    zoom = peewee.IntegerField(null=False, default=3)
    marker = peewee.IntegerField(null=False, default=0)
    time_create = peewee.IntegerField(null=False, default=0)
    time_update = peewee.IntegerField(null=False, default=0)
    public = peewee.IntegerField(null=False, default=0)
