'''
Handler of Posts via Ajax.
'''
import json

import tornado.escape
import tornado.web

import config
from config import CMS_CFG
from torcms.core import privilege, tools
from torcms.handlers.post_handler import PostHandler
from torcms.model.category_model import MCategory
from torcms.model.post_model import MPost
from torcms.model.label_model import MPost2Label
from torcms.model.post2catalog_model import MPost2Catalog
from torcms.core.tools import logger
from torcms.model.post_hist_model import MPostHist
from torcms.model.user_model import MUser


def update_category(uid, post_data):
    '''
    Update the category of the post.
    :param uid:  The ID of the post. Extra info would get by requests.
    '''

    # deprecated
    # catid = kwargs['catid'] if MCategory.get_by_uid(kwargs.get('catid')) else None
    # post_data = self.get_request_arguments()

    '''
    在前端，使用 `gcat0`，`gcat1`，`gcat2` 等，作为分类的参数。
    因为一个 post 可能会有多个分类，再定义第1分类的 key ：
        'def_cat_uid'： 第1分类
        'def_cat_pid' : 分1分类的父类
    '''
    if 'gcat0' in post_data:
        pass
    else:
        return False

    # Used to update MPost2Category, to keep order.
    the_cats_arr = []
    # Used to update post extinfo.
    the_cats_dict = {}

    # for old page. deprecated
    # def_cate_arr.append('def_cat_uid')

    def_cate_arr = ['gcat{0}'.format(x) for x in range(10)]
    for key in def_cate_arr:
        if key not in post_data:
            continue
        if post_data[key] == '' or post_data[key] == '0':
            continue
        # 有可能选重复了。保留前面的
        if post_data[key] in the_cats_arr:
            continue

        the_cats_arr.append(post_data[key] + ' ' * (4 - len(post_data[key])))
        the_cats_dict[key] = post_data[key] + ' ' * (4 - len(post_data[key]))

    # if catid:
    #     def_cat_id = catid
    if the_cats_arr:
        def_cat_id = the_cats_arr[0]
    else:
        def_cat_id = None

    if def_cat_id:
        the_cats_dict['gcat0'] = def_cat_id
        the_cats_dict['def_cat_uid'] = def_cat_id
        the_cats_dict['def_cat_pid'] = MCategory.get_by_uid(def_cat_id).pid

    logger.info('Update category: {0}'.format(the_cats_arr))
    logger.info('Update category: {0}'.format(the_cats_dict))

    # Add the category
    MPost.update_jsonb(uid, the_cats_dict)

    for index, idx_catid in enumerate(the_cats_arr):
        MPost2Catalog.add_record(uid, idx_catid, index)

    # Delete the old category if not in post requests.
    current_infos = MPost2Catalog.query_by_entity_uid(uid, kind='').objects()
    for cur_info in current_infos:
        if cur_info.tag_id not in the_cats_arr:
            MPost2Catalog.remove_relation(uid, cur_info.tag_id)


def update_label(post_id, post_data):
    '''
    Update the label when updating.
    '''
    current_tag_infos = MPost2Label.get_by_uid(post_id).objects()
    if 'tags' in post_data:
        pass
    else:
        return False

    tags_arr = [x.strip() for x in post_data['tags'].split(',')]
    for tag_name in tags_arr:
        if tag_name == '':
            pass
        else:
            MPost2Label.add_record(post_id, tag_name, 1)

    for cur_info in current_tag_infos:
        if cur_info.tag_name in tags_arr:
            pass
        else:
            MPost2Label.remove_relation(post_id, cur_info.tag_id)


class PostAjaxHandler(PostHandler):
    '''
    Handler of Posts via Ajax.
    '''

    def initialize(self, **kwargs):
        super().initialize()

    def get(self, *args, **kwargs):
        url_str = args[0]
        url_arr = self.parse_url(args[0])
        if url_arr[0] in ['_delete', 'delete']:
            self.j_delete(url_arr[1])

        if len(url_arr) == 2:
            if url_arr[0] == 'recent':
                self.p_recent(url_arr[1])
            elif url_arr[0] in ['nullify', 'update_valid']:
                self.j_nullify(url_arr[1])

        elif len(url_arr) == 3:
            self.p_recent(url_arr[1], url_arr[2])

        elif len(url_arr) == 1 and len(url_str) >= 4:
            self._view_or_add(url_str)

    def post(self, *args, **kwargs):
        url_str = args[0]
        url_arr = self.parse_url(url_str)

        if len(url_arr) == 3 and url_arr[0] == 'update_state':
            print('=========')
            print(url_arr[1], url_arr[2])
            self.update_state(url_arr[1], url_arr[2])

        if url_str == 'j_add':
            self.json_add()
        elif url_str == 'j_view':
            self.json_view()
        elif url_arr[0] == 'j_edit':
            self.json_edit(url_arr[1])

        elif url_str == 'j_recent':
            self.json_recent()

    def viewinfo(self, postinfo):
        '''
        View the info
        '''
        out_json = {
            'uid': postinfo.uid,
            'time_update': postinfo.time_update,
            'title': postinfo.title,
            'cnt_html': tornado.escape.xhtml_unescape(postinfo.cnt_html)
        }
        self.write(json.dumps(out_json))

    def p_recent(self, kind, cur_p='', with_catalog=True, with_date=True):
        '''
        List posts that recent edited, partially.
        '''
        current_page_number = 1
        if cur_p == '':
            current_page_number = 1
        else:
            try:
                current_page_number = int(cur_p)
            except TypeError:
                current_page_number = 1
            except Exception as err:
                print(err.args)
                print(str(err))
                print(repr(err))

        current_page_number = 1 if current_page_number < 1 else current_page_number

        # pager_num = int(MPost.total_number(kind) / CMS_CFG['list_num'])
        kwd = {
            'pager': '',
            'title': 'Recent posts.',
            'with_catalog': with_catalog,
            'with_date': with_date,
            'kind': kind,
            'current_page': current_page_number,
            'post_count': MPost.get_counts(),
            'router': config.router_post[kind],
        }
        self.render(
            'admin/post_ajax/post_list.html',
            kwd=kwd,
            view=MPost.query_recent(num=20, kind=kind),
            infos=MPost.query_pager_by_slug(
                kind=kind, current_page_num=current_page_number),
            format_date=tools.format_date,
            userinfo=self.userinfo,
            cfg=CMS_CFG,
        )

    @tornado.web.authenticated
    @privilege.auth_delete
    def j_delete(self, *args):
        '''
        Delete the post, but return the JSON.
        '''

        uid = args[0]

        current_infor = MPost.get_by_uid(uid)
        tslug = MCategory.get_by_uid(current_infor.extinfo['def_cat_uid'])
        is_deleted = MPost.delete(uid)
        MCategory.update_count(current_infor.extinfo['def_cat_uid'])
        if is_deleted:
            output = {
                'del_info': 1,
                'cat_slug': tslug.slug,
                'cat_id': tslug.uid,
                'kind': current_infor.kind
            }
        else:
            output = {
                'del_info': 0,
            }
        return json.dump(output, self)

    @tornado.web.authenticated
    @privilege.auth_delete
    def j_nullify(self, *args):
        '''
        update valid, but return the JSON.
        '''

        uid = args[0]
        current_infor = MPost.get_by_uid(uid)
        tslug = MCategory.get_by_uid(current_infor.extinfo['def_cat_uid'])
        is_deleted = MPost.nullify(uid)
        MCategory.update_count(current_infor.extinfo['def_cat_uid'])

        if is_deleted:
            output = {
                'nullify_info': 1,
                'cat_slug': tslug.slug,
                'cat_id': tslug.uid,
                'kind': current_infor.kind
            }
        else:
            output = {
                'nullify_info': 0,
            }
        return json.dump(output, self)

    def update_state(self, infoid, state):
        postinfo = MPost.get_by_uid(infoid)

        if state[1] in ['0', '1']:
            if postinfo and postinfo.user_name == self.userinfo.user_name:
                is_true = MPost.update_state(infoid, state)
            else:
                is_true = False
        elif state[1] in ['2', '3']:

            if self.userinfo.role[2] >= '1':
                is_true = MPost.update_state(infoid, state)
                if state[1] == '2':
                    MPost.update_valid(infoid)
                else:
                    MPost.nullify(infoid)

            else:
                is_true = False
        else:
            is_true = False
        output = {'state': state}
        if is_true:
            return json.dump(output, self)
        else:
            return False

    @tornado.web.authenticated
    def json_add(self):

        '''
        in infor.
        '''

        uid = self._gen_uid()

        post_data, ext_dic = self.__parse_post_data()

        title = post_data['title'].strip()

        if len(title) < 2:
            output = {
                'info': 'Title cannot be less than 2 characters',
                'code': '0'
            }
            return json.dump(output, self)

        if 'valid' in post_data:
            post_data['valid'] = int(post_data['valid'])
        else:
            post_data['valid'] = 1

        # 在应用中，会有分类的逻辑，需要处理
        if 'gcat0' in post_data:
            pass
        else:
            output = {
                'info': 'Please select a category',
                'code': '-1'
            }
            return json.dump(output, self)
        ext_dic['def_uid'] = uid  # 此 key 用于更新文档时在历史记录中跟踪原 uid .
        ext_dic['gcat0'] = post_data['gcat0']
        ext_dic['def_cat_uid'] = post_data['gcat0']

        # MPost中并没有分类的逻辑关系
        MPost.add_or_update_post(uid, post_data, extinfo=ext_dic)
        # kwargs.pop('uid', None)  # delete `uid` if exists in kwargs

        self._add_download_entity(ext_dic)

        update_category(uid, post_data)
        update_label(uid, post_data)
        # self.update_label(uid)

        # cele_gen_whoosh.delay()

        tornado.ioloop.IOLoop.instance().add_callback(self.cele_gen_whoosh)
        output = {
            'info': 'Added successfully',
            'code': '1',
            'uid': uid
        }
        return json.dump(output, self)

    def __parse_post_data(self):
        '''
        fetch post accessed data. post_data, and ext_dic.
        '''
        post_data = {}
        ext_dic = {}
        for key in self.request.arguments:
            if key.startswith('ext_') or key.startswith('tag_') or key.startswith('_tag_'):
                ext_dic[key] = self.get_argument(key, default='')
            else:
                post_data[key] = self.get_arguments(key)[0]

        post_data['user_name'] = 'admin'
        post_data['kind'] = self.kind

        # append external infor.

        if 'tags' in post_data:
            ext_dic['def_tag_arr'] = [
                x.strip()
                for x in post_data['tags'].strip().strip(',').split(',')
            ]
        ext_dic = dict(ext_dic, **self.ext_post_data(postdata=post_data))

        return (post_data, ext_dic)

    def json_view(self):
        post_data = self.get_request_arguments()
        uid = post_data.get('uid', '')
        postinfo = MPost.get_by_uid(uid)
        if postinfo:

            output = {
                'code': '1',
                'info': 'successful',
                'uid': postinfo.uid,
                'logo': postinfo.logo,
                'time_update': postinfo.time_update,
                'title': postinfo.title,
                'cnt_html': tornado.escape.xhtml_unescape(postinfo.cnt_html),
                'cnt_md': postinfo.cnt_md
            }

            return json.dump(output, self)
        else:
            output = {
                'code': '0',
                'info': 'failed'
            }
            return json.dump(output, self)

    @tornado.web.authenticated
    def json_edit(self, uid):
        '''
        in infor.
        '''
        print("/*" * 50)
        print(uid)

        postinfo = MPost.get_by_uid(uid)
        if postinfo.kind == self.kind:
            pass
        else:
            return False

        post_data, ext_dic = self.__parse_post_data()
        post_data['user_name'] = 'admin'
        self.userinfo = MUser.get_by_name('admin')
        if 'gcat0' in post_data:
            pass
        else:
            output = {
                'info': 'Please select a category',
                'code': '-1'
            }
            return json.dump(output, self)

        if 'valid' in post_data:
            post_data['valid'] = int(post_data['valid'])
        else:
            post_data['valid'] = postinfo.valid

        ext_dic['def_uid'] = uid

        cnt_old = tornado.escape.xhtml_unescape(postinfo.cnt_md).strip()
        cnt_new = post_data['cnt_md'].strip()
        if cnt_old == cnt_new:
            pass
        else:
            MPostHist.create_post_history(postinfo, self.userinfo)

        MPost.add_or_update_post(uid, post_data, extinfo=ext_dic)

        # todo:应该判断当前审核状态，是否可以进行修改状态。
        if self.userinfo.user_name == postinfo.user_name and postinfo.state == 'b000':
            MPost.update_state(uid, 'a000')

        self._add_download_entity(ext_dic)
        # self.update_tag(uid=uid)

        update_category(uid, post_data)
        update_label(uid, post_data)
        # self.update_label(uid)

        logger.info('post kind:' + self.kind)
        # cele_gen_whoosh.delay()
        tornado.ioloop.IOLoop.instance().add_callback(self.cele_gen_whoosh)

        output = {
            'code': '1',
            'info': 'successful',
            'uid': postinfo.uid,

        }

        return json.dump(output, self)

    def json_recent(self):
        '''
        List posts that recent edited, partially.
        '''

        post_data = self.get_request_arguments()
        kind = post_data.get('kind', 1)
        cur_p = post_data.get('cur_p', '')
        with_catalog = post_data.get('with_catalog', True)
        with_date = post_data.get('with_date', True)

        current_page_number = 1
        if cur_p == '':
            current_page_number = 1
        else:
            try:
                current_page_number = int(cur_p)
            except TypeError:
                current_page_number = 1
            except Exception as err:
                print(err.args)
                print(str(err))
                print(repr(err))

        current_page_number = 1 if current_page_number < 1 else current_page_number

        recs = MPost.query_recent(num=20, kind=kind)
        rec_arr = []

        for rec in recs:
            rec_arr.append({'title': rec.title, 'uid': rec.uid, 'cnt_md': rec.cnt_md})

        output = {
            'code': '1',
            'info': 'successful',
            'recs': rec_arr,
            'current_page_number': current_page_number,

        }

        return json.dump(output, self)
