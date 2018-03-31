# -*- coding: utf-8 -*-

'''
for database schema migration.

Memo for Usage:
    migrate.migrate(torcms_migrator.rename_table('e_layout', 'mablayout'))
    migrate.migrate(torcms_migrator.drop_column('tabtag', 'role_mask'))
'''
from playhouse import migrate
from playhouse.postgres_ext import BinaryJSONField
import config


def run_migrate(*args):
    '''
    running some migration.
    :return:
    '''

    print('Begin migrate ...')

    torcms_migrator = migrate.PostgresqlMigrator(config.DB_CON)

    memo_field = migrate.TextField(null=False, default='', help_text='Memo', )
    try:
        migrate.migrate(torcms_migrator.add_column('tabpost', 'memo', memo_field))
    except:
        pass

    desc_field = migrate.CharField(null=False, default='', max_length=255, help_text='')
    try:
        migrate.migrate(torcms_migrator.add_column('tabentity', 'desc', desc_field))
    except:
        pass

    extinfo_field = BinaryJSONField(null=False, default={}, help_text='Extra data in JSON.')
    try:
        migrate.migrate(torcms_migrator.add_column('tabmember', 'extinfo', extinfo_field))
    except:
        pass

    par_id_field = migrate.CharField(null=False, default='', max_length=4,
                                     help_text='父类id，对于label，top_id为""')
    try:
        migrate.migrate(torcms_migrator.add_column('tabpost2tag', 'par_id', par_id_field))
    except:
        pass

    print('Migration finished.')
