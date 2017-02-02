# -*- coding: utf-8 -*-

from playhouse import migrate
import config

def run_migrate():
    print('Begin migrate ...')
    torcms_migrator = migrate.PostgresqlMigrator(config.dbconnect)
    float_field = migrate.FloatField(null=False, default=5)
    try:
        migrate.migrate(torcms_migrator.add_column('g_post', 'rating', float_field))
    except:
        pass

    pid = migrate.CharField(null=False, max_length=4, default='xxxx', help_text='parent id')
    tmpl = migrate.IntegerField(null=False, default=9, help_text='tmplate type')

    try:
        migrate.migrate(torcms_migrator.add_column('g_tag', 'pid', pid))
    except:
        pass

    try:
        migrate.migrate(torcms_migrator.add_column('g_tag', 'tmpl', tmpl))
    except:
        pass

    try:
        migrate.migrate(torcms_migrator.drop_column('g_tag', 'role_mask'))
    except:
        pass

    print('QED')
