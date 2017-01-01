# -*- coding:utf-8 -*-

import config
import peewee

# create a base model class that our application's models will extend. From django
class BaseModel(peewee.Model):
    class Meta:
        database = config.dbconnect
