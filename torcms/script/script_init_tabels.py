# -*- coding: utf-8 -*-

'''
initialize table.s
'''

from .script_funcs import postgres_svr
from playhouse import migrate
from playhouse.postgres_ext import BinaryJSONField

import config
from torcms.model.core_tab import TabPost, TabTag, TabMember, TabWiki, TabLink, TabEntity, \
    TabPostHist, TabWikiHist, TabCollect, TabPost2Tag, TabRel, TabEvaluation, TabUsage, TabReply, \
    TabUser2Reply, TabRating, TabEntity2User, TabLog, TabReplyid,TabReferrer


def create_table(the_table):
    '''
    Create a certain table.
    '''
    try:
        the_table.create_table()
    except:
        pass


def run_init_tables(*args):
    '''
    Run to init tables.
    '''
    print('--')
    print('Create tables ...')
    create_table(TabPost)
    create_table(TabTag)
    create_table(TabMember)
    create_table(TabWiki)
    create_table(TabLink)
    create_table(TabEntity)
    create_table(TabPostHist)
    create_table(TabWikiHist)
    create_table(TabCollect)
    create_table(TabPost2Tag)
    create_table(TabRel)
    create_table(TabEvaluation)
    create_table(TabUsage)
    create_table(TabReply)
    create_table(TabUser2Reply)
    create_table(TabRating)
    create_table(TabEntity2User)
    create_table(TabLog)
    create_table(TabReplyid)
    create_table(TabReferrer)
    print('Creating tables finished.')
    run_migrate()

def run_migrate(*args):
    '''
    for database schema migration.
    Memo for Usage:
        migrate.migrate(torcms_migrator.rename_table('e_layout', 'mablayout'))
        migrate.migrate(torcms_migrator.drop_column('tabtag', 'role_mask'))
    '''

    '''
    在psql状态下查询表结构
    \d
    tablename
    '''


    conn, cur = postgres_svr()

    cur = conn.cursor()
    cur.execute('''alter table tabmember alter column user_name type character varying(255)''')
    print(    "Table TabMember altered successfully")

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

    category_field = migrate.CharField(null=False, default='0', max_length=1,
                                       help_text='0为评论，1为回复')
    try:
        migrate.migrate(torcms_migrator.add_column('tabreply', 'category', category_field))
    except:
        pass

    try:
        migrate.migrate(torcms_migrator.drop_column('tabentity2user', 'count'))
        # print('删除字段成功：count.')
    except:
        pass

    user_ip_field = migrate.CharField(null=False, default='0', help_text='User IP Address', )
    try:
        migrate.migrate(torcms_migrator.add_column('tabentity2user', 'user_ip', user_ip_field))
        # print('添加字段成功：user_ip.')
    except:
        pass

    view_count_1d = migrate.IntegerField(default=0, help_text='24小时内阅读量')
    try:
        migrate.migrate(torcms_migrator.add_column('tabpost', 'access_1d', view_count_1d))
    except:
        pass

    view_count_7d = migrate.IntegerField(default=0, help_text='7*24小时内阅读量')
    try:
        migrate.migrate(torcms_migrator.add_column('tabpost', 'access_7d', view_count_7d))
    except:
        pass

    view_count_30d = migrate.IntegerField(default=0, help_text='30*24小时内阅读量')
    try:
        migrate.migrate(torcms_migrator.add_column('tabpost', 'access_30d', view_count_30d))
    except:
        pass


    print('Migration finished.')