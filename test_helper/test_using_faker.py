# -*- coding: utf-8

'''
导入faker模拟数据信息
'''

from faker import Faker
from torcms.model.category_model import MCategory
from torcms.model.post2catalog_model import MPost2Catalog
from torcms.model.post_model import MPost
from torcms.model.label_model import MPost2Label
from torcms.core.tools import get_uu4d
from torcms.handlers.post_handler import import_post


def update_category(uid, postdata, kwargs):
    '''
    Update the category of the post.
    '''
    catid = kwargs['catid'] if ('catid' in kwargs and MCategory.get_by_uid(kwargs['catid'])) else None

    post_data = postdata

    current_infos = MPost2Catalog.query_by_entity_uid(uid, kind='').objects()

    new_category_arr = []
    # Used to update post2category, to keep order.
    def_cate_arr = ['gcat{0}'.format(x) for x in range(10)]

    # for old page.
    def_cate_arr.append('def_cat_uid')

    # Used to update post extinfo.
    cat_dic = {}
    for key in def_cate_arr:
        if key not in post_data:
            continue
        if post_data[key] == '' or post_data[key] == '0':
            continue
        # 有可能选重复了。保留前面的
        if post_data[key] in new_category_arr:
            continue

        new_category_arr.append(post_data[key] + ' ' * (4 - len(post_data[key])))
        cat_dic[key] = post_data[key] + ' ' * (4 - len(post_data[key]))

    if catid:
        def_cat_id = catid
    elif new_category_arr:
        def_cat_id = new_category_arr[0]
    else:
        def_cat_id = None

    if def_cat_id:
        cat_dic['def_cat_uid'] = def_cat_id
        cat_dic['def_cat_pid'] = MCategory.get_by_uid(def_cat_id).pid

    MPost.update_jsonb(uid, cat_dic)

    for index, catid in enumerate(new_category_arr):
        MPost2Catalog.add_record(uid, catid, index)

    # Delete the old category if not in post requests.
    for cur_info in current_infos:
        if cur_info.tag_id not in new_category_arr:
            MPost2Catalog.remove_relation(uid, cur_info.tag_id)

def update_label(signature, post_data):
    '''
    Update the label .
    '''
    current_tag_infos = MPost2Label.get_by_uid(signature).objects()
    if 'tags' in post_data:
        pass
    else:
        return False

    if '；' in post_data['tags']:
        tags_arr = [x.strip() for x in post_data['tags'].split('；')]
    elif ',' in post_data['tags']:
        tags_arr = [x.strip() for x in post_data['tags'].split(',')]
    elif '，' in post_data['tags']:
        tags_arr = [x.strip() for x in post_data['tags'].split('，')]
    elif ';' in post_data['tags']:
        tags_arr = [x.strip() for x in post_data['tags'].split(';')]
    else:
        tags_arr = [x.strip() for x in post_data['tags'].split(' ')]

    if len(tags_arr) > 5:
        del tags_arr[5:]

    for tag_name in tags_arr:
        if tag_name == '':
            pass
        else:
            MPost2Label.add_record(signature, tag_name, 1)

    for cur_info in current_tag_infos:
        if cur_info.tag_name in tags_arr:
            pass
        else:
            MPost2Label.remove_relation(signature, cur_info.tag_id)


def test_meta():
    # 初始化Faker
    f = Faker(locale='zh_CN')

    for ii in range(10):
        uid = '3' + get_uu4d()
        while MPost.get_by_uid(uid):
            uid = '3' + get_uu4d()
        ext_dic = {}
        post_data = {}

        post_data['valid'] = 0
        post_data['title'] = f.company_prefix()
        post_data['cnt_md'] = f.text()
        post_data['user_name'] = 'admin'
        post_data['kind'] = '3'

        ext_dic['def_uid'] = uid
        ext_dic['gcat0'] = '3101'
        ext_dic['def_cat_uid'] = '3101'

        kwargsa = {
            'gcat0': '3101',
            'cat_id': '3100',
        }
        import_post(uid, post_data, extinfo=ext_dic)
        # MPost.add_or_update_post(uid,post_data,extinfo=ext_dic)
        # update_category(uid, post_data, kwargsa)
        # update_label(uid, post_data)

