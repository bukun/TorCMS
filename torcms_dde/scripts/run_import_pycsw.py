'''
从 Records 表中同步数据到 TabPost .
'''

import psycopg2
from pprint import pprint

from torcms.core import tools
from torcms.model.post_model import MPost
from torcms.model.post2catalog_model import MPost2Catalog

from torcms.handlers.post_handler import update_category,update_label

from torcms.model.core_tab import TabPost

from cfg import DB_CFG

PYCSW_DB_FIELD = [
    'identifier',
    'typename',
    'schema',
    'mdsource',
    'insert_date',
    'xml',
    'anytext',
    'language',
    'type',
    'title',
    'title_alternate',
    'abstract',
    'keywords',
    'keywordstype',
    'parentidentifier',
    'relation',
    'time_begin',
    'time_end',
    'topicategory',
    'resourcelanguage',
    'creator',
    'publisher',
    'contributor',
    'organization',
    'securityconstraints',
    'accessconstraints',
    'otherconstraints',
    'date',
    'date_revision',
    'date_creation',
    'date_publication',
    'date_modified',
    'format',
    'source',
    'crs',
    'geodescode',
    'denominator',
    'distancevalue',
    'distanceuom',
    'wkt_geometry',
    'servicetype',
    'servicetypeversion',
    'operation',
    'couplingtype',
    'operateson',
    'operatesonidentifier',
    'operatesoname',
    'degree',
    'classification',
    'conditionapplyingtoaccessanduse',
    'lineage',
    'responsiblepartyrole',
    'specificationtitle',
    'specificationdate',
    'specificationdatetype',
    'links',
]


def insert_into_tabpost(catid, rec):
    '''
    在 TabPost 中创建或更新数据
    '''

    dde_dict = {
        'pycsw_identifier': rec[0],
        'pycsw_typename': rec[1],
        'pycsw_schema': rec[2],
        'pycsw_mdsource': rec[3],
        'pycsw_insert_date': rec[4],
        'pycsw_xml': rec[5],
        'pycsw_anytext': rec[6],
        'pycsw_language': rec[7],
        'pycsw_type': rec[8],
        'pycsw_title': rec[9],
        'pycsw_title_alternate': rec[10],
        'pycsw_abstract': rec[11],
        'pycsw_keywords': rec[12],
        'pycsw_keywordstype': rec[13],
        'pycsw_parentidentifier': rec[14],
        'pycsw_relation': rec[15],
        'pycsw_time_begin': rec[16],
        'pycsw_time_end': rec[17],
        'pycsw_topicategory': rec[18],
        'pycsw_resourcelanguage': rec[19],
        'pycsw_creator': rec[20],
        'pycsw_publisher': rec[21],
        'pycsw_contributor': rec[22],
        'pycsw_organization': rec[23],
        'pycsw_securityconstraints': rec[24],
        'pycsw_accessconstraints': rec[25],
        'pycsw_otherconstraints': rec[26],
        'pycsw_date': rec[27],
        'pycsw_date_revision': rec[28],
        'pycsw_date_creation': rec[29],
        'pycsw_date_publication': rec[30],
        'pycsw_date_modified': rec[31],
        'pycsw_format': rec[32],
        'pycsw_source': rec[33],
        'pycsw_crs': rec[34],
        'pycsw_geodescode': rec[35],
        'pycsw_denominator': rec[36],
        'pycsw_distancevalue': rec[37],
        'pycsw_distanceuom': rec[38],
        'pycsw_wkt_geometry': rec[39],
        'pycsw_servicetype': rec[40],
        'pycsw_servicetypeversion': rec[41],
        'pycsw_operation': rec[42],
        'pycsw_couplingtype': rec[43],
        'pycsw_operateson': rec[44],
        'pycsw_operatesonidentifier': rec[45],
        'pycsw_operatesoname': rec[46],
        'pycsw_degree': rec[47],
        'pycsw_classification': rec[48],
        'pycsw_conditionapplyingtoaccessanduse': rec[49],
        'pycsw_lineage': rec[50],
        'pycsw_responsiblepartyrole': rec[51],
        'pycsw_specificationtitle': rec[52],
        'pycsw_specificationdate': rec[53],
        'pycsw_specificationdatetype': rec[54],
        'pycsw_links': rec[55],
        # 'pycsw_wkb_geometry': rec[56],
    }

    if rec[9]:
        pass
    else:
        return

    inrec = TabPost.select().where(TabPost.memo == rec[0])
    if 1 == 2 :
        # 如果在 TabPost 中已有，则跳过
        pass
    else:
        kind = 'd'
        # sig = kind + tools.get_uu4d()
        sig = rec[0]

        print('=' * 40)
        print(sig)

        # pprint(dde_dict)

        pp_data = {}
        pp_data['title'] = rec[9][:255]
        pp_data['cnt_md'] = rec[11] if rec[11] else rec[9]
        pp_data['user_name'] = 'admin'
        # pp_data['tags'] = rec[12]
        pp_data['def_cat_uid'] = catid
        pp_data['gcat0'] = catid
        pp_data['logo'] = ''
        pp_data['kind'] = kind
        pp_data['gcat0'] = catid
        pp_data['def_cat_pid'] = catid[:2] + '00'
        pp_data['memo'] = rec[0]
        pp_data['extinfo'] = {}
        pp_data['extinfo'].update(dde_dict)

        if pp_data.get('tags'):
            pp_data['extinfo']['def_tag_arr'] = [
                x.strip() for x in pp_data['tags'].strip().strip(',').split(',')
            ]
        print('dodo')
        print(pp_data)
        MPost.add_or_update(sig, pp_data)
        MPost.update_misc(sig, kind = 'd')

        # cate_rec = MPost2Catalog.get_first_category(sig )
        # if 1== 2:
        #     # 如果已经分类
        #     pass
        # else:
        #     print('dodo2')
        #     update_category(sig, pp_data)
        update_label(sig, pp_data)


def fetch_pycsw():
    '''
    获取 pycsw 中的记录，并进行处理。
    '''
    conn = psycopg2.connect(
        database=DB_CFG['db'],
        user=DB_CFG['db'],
        password=DB_CFG['pass'],
        host=DB_CFG['host'],
        port=DB_CFG.get('port', 5432)
    )

    cur = conn.cursor()
    cmd = "SELECT {} from Records".format(','.join(PYCSW_DB_FIELD)).strip(',')
    # print(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    idx = 0
    for row in rows:
        idx = idx + 1

        # insert_into_tabpost('0701', row)
        # insert_into_tabpost('a301', row)
        print('=' * 40)
        # print(row)
        print('=' * 40)

        # insert_into_tabpost('2501', row)
        insert_into_tabpost('d101', row)


if __name__ == '__main__':

    fetch_pycsw()

    new_dict = {}
    for idx, val in enumerate(PYCSW_DB_FIELD):
        pass
