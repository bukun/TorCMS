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

    print('Rename Table g_Tag')
    # torcms_migrator.rename_table('g_tag', 'TabTag')
    # migrate.migrate(
    #     torcms_migrator.rename_table('TabTag', 'tabtag')
    # )


    try:

        migrate.migrate(
            torcms_migrator.rename_table('g_tag', 'tabtag')
        )
    except:
        pass
    try:
        migrate.migrate(
            torcms_migrator.rename_table('g_link', 'tablink')
        )
    except:
        pass

    try:
        migrate.migrate(
            torcms_migrator.rename_table('g_post', 'tabpost')
        )
    except:
        pass
    try:
        migrate.migrate(
            torcms_migrator.rename_table('g_wiki', 'tabwiki')
        )
    except:
        pass
    try:
        migrate.migrate(
            torcms_migrator.rename_table('g_posthist', 'tabposthist')
        )
    except:
        pass
    try:
        migrate.migrate(
            torcms_migrator.rename_table('g_wikihist', 'tabwikihist')
        )
    except:
        pass
    try:
        migrate.migrate(
            torcms_migrator.rename_table('g_member', 'tabmember')
        )
    except:
        pass
    try:
        migrate.migrate(
            torcms_migrator.rename_table('g_entity', 'tabentity')
        )
    except:
        pass
    try:
        migrate.migrate(
            torcms_migrator.rename_table('g_post2tag', 'tabpost2tag')
        )
    except:
        pass
    try:
        migrate.migrate(
            torcms_migrator.rename_table('g_reply', 'tabreply')
        )
    except:
        pass

    try:
        migrate.migrate(
            torcms_migrator.rename_table('g_user2reply', 'tabuser2reply')
        )
    except:
        pass

    try:
        migrate.migrate(
            torcms_migrator.rename_table('g_collect', 'tabcollect')
        )
    except:
        pass
    try:
        migrate.migrate(
            torcms_migrator.rename_table('g_evaluation', 'tabevaluation')
        )
    except:
        pass

    try:
        migrate.migrate(
            torcms_migrator.rename_table('g_rating', 'tabrating')
        )
    except:
        pass
    try:
        migrate.migrate(
            torcms_migrator.rename_table('g_rating', 'tabrating')
        )
    except:
        pass
    try:
        migrate.migrate(
            torcms_migrator.rename_table('g_usage', 'tabusage')
        )
    except:
        pass
    try:
        migrate.migrate(
            torcms_migrator.rename_table('g_rel', 'tabrel')
        )
    except:
        pass

    # For Map
    try:
        migrate.migrate(
            torcms_migrator.rename_table('e_json', 'mabgson')
        )
    except:
        pass

    try:
        migrate.migrate(
            torcms_migrator.rename_table('e_post2json', 'mabpost2gson')
        )
    except:
        pass

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
