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

    # try:
    #     migrate.migrate(
    #         torcms_migrator.rename_table('e_layout', 'mablayout')
    #     )
    # except:
    #     pass

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

    # try:
    #     migrate.migrate(torcms_migrator.drop_column('tabtag', 'role_mask'))
    # except:
    #     pass

    print('QED')
