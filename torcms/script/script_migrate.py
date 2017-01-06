# -*- coding: utf-8 -*-

from playhouse.migrate import *
from playhouse.postgres_ext import BinaryJSONField
import config


def run_migrate():
    print('Begin migrate ...')
    migrator = PostgresqlMigrator(config.dbconnect)
    status_field = IntegerField(null=False, default=0)
    float_field = FloatField(null= False, default=5)
    try:
        migrate(migrator.add_column('g_post', 'rating', float_field))
    except:
        pass

    pid = CharField(null=False, max_length=4, default='xxxx', help_text='parent id')
    tmpl = IntegerField(null=False, default=9, help_text='tmplate type')

    try:
        migrate(migrator.add_column('g_tag', 'pid', pid))
    except:
        pass

    try:
        migrate(migrator.add_column('g_tag', 'tmpl', tmpl))
    except:
        pass

    try:
        migrate(migrator.drop_column('g_tag', 'role_mask'))
    except:
        pass


    print('QED')
