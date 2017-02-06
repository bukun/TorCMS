# -*- coding:utf-8 -*-

'''
create a base model class that our application's models will extend. From django
'''
import config
import peewee

class BaseModel(peewee.Model):
    '''
    base model
    '''
    class Meta:
        '''
        meta
        '''
        database = config.DB_CON
