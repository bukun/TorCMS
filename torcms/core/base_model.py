# -*- coding:utf-8 -*-
'''
create a base model class that our application's models will extend. From django
'''
import peewee

import config


class BaseModel(peewee.Model):
    '''
    base model
    '''

    # pylint: disable=no-value-for-parameter

    class Meta:
        '''
        meta
        '''
        # pylint: disable=no-value-for-parameter
        database = config.DB_CON
