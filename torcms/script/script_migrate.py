# -*- coding: utf-8 -*-

from playhouse import migrate
import config


def run_migrate(*args):
    '''
    running some migration.
    :return:
    '''

    print('Begin migrate ...')

    torcms_migrator = migrate.PostgresqlMigrator(config.DB_CON)


    try:
        migrate.migrate(
            torcms_migrator.rename_table('e_layout', 'mablayout')
        )
    except:
        pass

    float_field = migrate.FloatField(null=False, default=5)
    try:
        migrate.migrate(torcms_migrator.add_column('tabpost', 'rating', float_field))
    except:
        pass

    order = migrate.CharField(null=False, default='', max_length=8)

    try:
        migrate.migrate(torcms_migrator.add_column('tabpost', 'order', order))
    except:
        pass

    pid = migrate.CharField(null=False, max_length=4, default='xxxx', help_text='parent id')
    tmpl = migrate.IntegerField(null=False, default=9, help_text='tmplate type')

    try:
        migrate.migrate(torcms_migrator.add_column('tabtag', 'pid', pid))
    except:
        pass

    try:
        migrate.migrate(torcms_migrator.add_column('tabtag', 'tmpl', tmpl))
    except:
        pass

    try:
        migrate.migrate(torcms_migrator.drop_column('tabtag', 'role_mask'))
    except:
        pass

    print('QED')
