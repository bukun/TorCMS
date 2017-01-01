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

    # try:
    #     migrate(migrator.add_column('tabapp', 'user_name',
    #                                 CharField(null=False, default='', max_length=36, help_text='UserName', )))
    # except:
    #     pass
    #
    # try:
    #     migrate(migrator.add_column('tabapp', 'logo', CharField(default='')))
    # except:
    #     pass
    #
    try:
        migrate(migrator.drop_column('g_tag', 'role_mask'))
    except:
        pass
    #
    # try:
    #     migrate(migrator.drop_column('cabpagehist', 'time_create'))
    # except:
    #     pass
    #
    # try:
    #     migrate(migrator.drop_column('cabpagehist', 'date'))
    # except:
    #     pass
    #
    # try:
    #     migrate(migrator.rename_column('cabpagehist', 'id_user', 'user_name'))
    # except:
    #     pass
    #
    # try:
    #     migrate(migrator.drop_column('cabwikihist', 'date'))
    # except:
    #     pass
    #
    # try:
    #     migrate(migrator.drop_column('cabwikihist', 'time_create'))
    # except:
    #     pass
    #
    # try:
    #     migrate(migrator.drop_column('cabposthist', 'id_spec'))
    # except:
    #     pass
    #
    # try:
    #     migrate(migrator.drop_column('cabposthist', 'id_cats'))
    # except:
    #     pass
    #
    # try:
    #     migrate(migrator.drop_column('cabposthist', 'date'))
    # except:
    #     pass
    #
    # try:
    #     migrate(migrator.drop_column('cabposthist', 'time_create'))
    # except:
    #     pass
    #
    #
    # try:
    #     migrate(migrator.drop_column('cabpost', 'id_cats', status_field))
    # except:
    #     pass
    #
    # try:
    #     migrate(migrator.drop_column('tabapp', 'id_cats', status_field))
    # except:
    #     pass
    # try:
    #     migrate(migrator.add_column('cabpost', 'valid', status_field))
    # except:
    #     pass
    #
    # ext_field = BinaryJSONField(default={})
    #
    # try:
    #     migrate(migrator.add_column('cabpost', 'extinfo', ext_field))
    # except:
    #     pass
    #
    # try:
    #     migrate(migrator.add_column('cabpost', 'type', status_field))
    # except:
    #     pass
    #
    # try:
    #     migrate(migrator.drop_column('cabmember', 'valid'))
    # except:
    #     pass
    #
    # try:
    #     migrate(migrator.add_column('cabcatalog', 'type', status_field))
    # except:
    #     pass
    #
    #
    # try:
    #     migrate(migrator.drop_column('cabwiki', 'src_type'))
    # except:
    #     pass
    #
    # try:
    #     migrate(migrator.add_column('cabwiki', 'type', status_field))
    # except:
    #     pass
    #
    # try:
    #     migrate(migrator.rename_column('cabwiki', 'slug', 'uid'))
    # except:
    #     pass
    #
    # try:
    #     migrate(migrator.drop_column('cabpage', 'src_type'))
    # except:
    #     pass
    #
    # try:
    #     migrate(migrator.drop_column('cabpost', 'src_type'))
    # except:
    #     pass
    #
    # try:
    #     migrate(migrator.add_column('cabmember', 'time_email', status_field))
    # except:
    #     pass
    #
    # try:
    #     migrate(migrator.add_column('cabmember', 'time_login', status_field))
    # except:
    #     pass
    # try:
    #     migrate(migrator.add_column('cabmember', 'time_create', status_field))
    # except:
    #     pass
    #
    # try:
    #     migrate(migrator.add_column('cabmember', 'time_update', status_field))
    # except:
    #     pass
    #
    # try:
    #     migrate(
    #         migrator.rename_column('cabmember', 'reset_passwd_timestamp', 'time_reset_passwd')
    #     )
    # except:
    #     pass

    print('QED')
