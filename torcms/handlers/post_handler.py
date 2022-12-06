# -*- coding:utf-8 -*-
'''
The basic HTML Page handler.
'''

import json
import random

from concurrent.futures import ThreadPoolExecutor

import tornado.escape
import tornado.gen
import tornado.ioloop
import tornado.web

from config import router_post
from torcms.core import privilege, tools
from torcms.core.base_handler import BaseHandler
from torcms.core.tool.sqlite_helper import MAcces
from torcms.core.tools import logger
from torcms.handlers.entity_handler import EntityHandler
from torcms.model.category_model import MCategory
from torcms.model.entity_model import MEntity
from torcms.model.evaluation_model import MEvaluation
from torcms.model.label_model import MPost2Label
from torcms.model.post2catalog_model import MPost2Catalog
from torcms.model.post_hist_model import MPostHist
from torcms.model.post_model import MPost
from torcms.model.relation_model import MRelation
from torcms.model.usage_model import MUsage


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


class PostHandler(BaseHandler):
    '''
    The basic HTML Page handler.
    '''
    executor = ThreadPoolExecutor(2)

    def initialize(self, **kwargs):
        super().initialize()
        self.kind = kwargs.get('kind', '1')
        self.filter_view = kwargs.get('filter_view', False)
        self.entity = EntityHandler

    def get(self, *args, **kwargs):
        url_str = args[0]
        url_arr = self.parse_url(url_str)
        # if url_arr:
        #     self._redirect(url_arr)

        if url_str == '' or url_str == 'index':
            self.index()
        elif url_arr[0] == '_cat_add':
            self._to_add(catid=url_arr[1])
        elif url_arr[0] == '_add':
            if len(url_arr) == 2:
                self._to_add(uid=url_arr[1])
            else:
                self._to_add()
        elif len(url_arr) == 1 and len(url_str) >= 4:
            self._view_or_add(url_str)
        elif len(url_arr) == 2:
            dict_get = {
                '_edit_kind': self._to_edit_kind,
                '_edit': self._to_edit,
                '_delete': self._delete,
            }
            dict_get.get(url_arr[0])(url_arr[1])
        else:
            self.show404()

    def post(self, *args, **kwargs):

        url_str = args[0]
        logger.info('Post url: {0}'.format(url_str))
        url_arr = self.parse_url(url_str)

        if url_arr[0] in ['_edit']:
            self.update(url_arr[1])
        elif url_arr[0] in ['_add']:
            if len(url_arr) == 2:
                self.add(uid=url_arr[1])
            else:
                self.add()
        elif url_arr[0] == '_edit_kind':
            self._change_kind(url_arr[1])
        elif url_arr[0] in ['_cat_add']:
            self.add(catid=url_arr[1])
        elif len(url_arr) == 1 and len(url_str) >= 4:
            self.add(uid=url_str)
        elif url_arr[0] == 'rel' and len(url_arr) == 3:
            self._add_relation(url_arr[1], url_arr[2])
        else:
            self.show404()

    def index(self):
        '''
        The default page of POST.
        '''
        if self.filter_view:
            tmpl = f'tmpl_{self.kind}/tpl_index.html'
        else:
            tmpl = f'post_{self.kind}/post_index.html'
        self.render(tmpl,
                    userinfo=self.userinfo,
                    kwd={'uid': '', })

    def _gen_uid(self):
        '''
        Generate the ID for post.
        :return: the new ID.
        '''
        cur_uid = self.kind + tools.get_uu4d()
        while MPost.get_by_uid(cur_uid):
            cur_uid = self.kind + tools.get_uu4d()
        return cur_uid

    def _get_tmpl_view(self, rec):
        '''
        According to the application, each info of it's classification could
        has different temaplate.
        :param rec: the App record.
        :return: the temaplte path.
        '''

        cat_id = self.__get_cat_id(rec)

        logger.info('For templates: catid: {0},  filter_view: {1}'.format(
            cat_id, self.filter_view))

        if cat_id and self.filter_view:
            tmpl = 'autogen/view/view_{0}.html'.format(cat_id)
        else:
            tmpl = 'post_{0}/post_view.html'.format(self.kind)
        return tmpl

    def __get_cat_id(self, postinfo):

        catinfo = MPost2Catalog.get_first_category(postinfo.uid)
        if catinfo:
            cat_id = catinfo.tag_id
        else:
            cat_id = None

        return cat_id

    @tornado.web.authenticated
    @privilege.auth_add
    def _to_add_with_category(self, catid):
        '''
        Used for info2.
        :param catid: the uid of category
        '''

        catinfo = MCategory.get_by_uid(catid)
        kwd = {
            'uid': self._gen_uid(),
            'userid': self.userinfo.user_name if self.userinfo else '',
            'gcat0': catid,
            'parentname': MCategory.get_by_uid(catinfo.pid).name,
            'catname': MCategory.get_by_uid(catid).name,
            'router': router_post[self.kind]
        }

        self.render('autogen/add/add_{0}.html'.format(catid),
                    userinfo=self.userinfo,
                    kwd=kwd)

    def _view_or_add(self, uid):
        '''
        Try to get the post. If not, to add the wiki.
        '''
        postinfo = MPost.get_by_uid(uid)
        if postinfo:
            if postinfo.kind == self.kind:
                self.viewinfo(postinfo)
            else:
                self.redirect(
                    '/{0}/{1}'.format(router_post[postinfo.kind], postinfo.uid),
                    permanent=True)

        elif self.userinfo:
            self._to_add(uid=uid)
        else:
            self.show404()

    @tornado.web.authenticated
    @privilege.auth_add
    def _to_add(self, **kwargs):
        '''
        Used for info1.
        '''

        if 'catid' in kwargs:
            catid = kwargs['catid']
            return self._to_add_with_category(catid)

        else:
            if 'uid' in kwargs and MPost.get_by_uid(kwargs['uid']):
                # todo:
                # self.redirect('/{0}/edit/{1}'.format(self.app_url_name, uid))
                uid = kwargs['uid']
            else:
                uid = ''
            self.render('post_{0}/post_add.html'.format(self.kind),
                        tag_infos=MCategory.query_all(by_order=True, kind=self.kind),
                        userinfo=self.userinfo,
                        kwd={
                            'uid': uid,

                        })

    @tornado.web.authenticated
    @privilege.auth_edit
    def _to_edit(self, infoid):
        '''
        render the HTML page for post editing.
        '''

        postinfo = MPost.get_by_uid(infoid)

        if postinfo:
            pass
        else:
            return self.show404()

        catid = self.__get_cat_id(postinfo)

        if catid and len(catid) == 4:
            pass
        else:
            catid = ''

        catinfo = None
        p_catinfo = None

        post2catinfo = MPost2Catalog.get_first_category(postinfo.uid)
        if post2catinfo:
            catid = post2catinfo.tag_id
            catinfo = MCategory.get_by_uid(catid)
            if catinfo:
                p_catinfo = MCategory.get_by_uid(catinfo.pid)

        kwd = {
            'gcat0': catid,
            'parentname': '',
            'catname': '',
            'parentlist': MCategory.get_parent_list(),
            'userip': self.request.remote_ip,
            'extinfo': json.dumps(postinfo.extinfo,
                                  indent=2,
                                  ensure_ascii=False),
            'router': router_post[postinfo.kind]
        }

        if self.filter_view:
            tmpl = 'autogen/edit/edit_{0}.html'.format(catid)
        else:
            tmpl = 'post_{0}/post_edit.html'.format(self.kind)

        logger.info('Meta template: {0}'.format(tmpl))

        self.render(tmpl,
                    kwd=kwd,
                    postinfo=postinfo,
                    catinfo=catinfo,
                    pcatinfo=p_catinfo,
                    userinfo=self.userinfo,
                    cat_enum=MCategory.get_qian2(catid[:2]),
                    tag_infos=MCategory.query_all(by_order=True,
                                                  kind=self.kind),
                    tag_infos2=MCategory.query_all(by_order=True,
                                                   kind=self.kind),
                    app2tag_info=MPost2Catalog.query_by_entity_uid(
                        infoid, kind=self.kind).objects(),
                    app2label_info=MPost2Label.get_by_uid(infoid).objects())

    def _gen_last_current_relation(self, post_id):
        '''
        Generate the relation for the post and last post viewed.
        '''
        last_post_id = self.get_secure_cookie('last_post_uid')
        if last_post_id:
            last_post_id = last_post_id.decode('utf-8')
        self.set_secure_cookie('last_post_uid', post_id)

        if last_post_id and MPost.get_by_uid(last_post_id):
            self._add_relation(last_post_id, post_id)

    @privilege.auth_view
    def viewinfo(self, postinfo):
        '''
        查看 Post.
        '''

        __ext_catid = postinfo.extinfo.get('def_cat_uid', '')
        cat_enum1 = MCategory.get_qian2(__ext_catid[:2]) if __ext_catid else []
        rand_recs, rel_recs = self.fetch_additional_posts(postinfo.uid)

        self._chuli_cookie_relation(postinfo.uid)

        catinfo = None
        p_catinfo = None

        post2catinfo = MPost2Catalog.get_first_category(postinfo.uid)
        if post2catinfo:
            catinfo = MCategory.get_by_uid(post2catinfo.tag_id)
            if catinfo:
                p_catinfo = MCategory.get_by_uid(catinfo.pid)

        kwd = self._the_view_kwd(postinfo)

        MPost.update_misc(postinfo.uid, count=True)
        MAcces.add(postinfo.uid)

        if self.get_current_user() and self.userinfo:
            MUsage.add_or_update(self.userinfo.uid, postinfo.uid,
                                 postinfo.kind)

        self.set_cookie('user_pass', kwd['cookie_str'])

        tmpl = self.ext_tmpl_view(postinfo)

        if self.userinfo:
            recent_apps = MUsage.query_recent(self.userinfo.uid, postinfo.kind,
                                              6).objects()[1:]
        else:
            recent_apps = []
        logger.info('The Info Template: {0}'.format(tmpl))

        self.render(
            tmpl,
            kwd=dict(kwd, **self.ext_view_kwd(postinfo)),
            postinfo=postinfo,
            userinfo=self.userinfo,
            catinfo=catinfo,
            pcatinfo=p_catinfo,
            relations=rel_recs,
            rand_recs=rand_recs,
            subcats=MCategory.query_sub_cat(p_catinfo.uid) if p_catinfo else '',
            ad_switch=random.randint(1, 18),
            tag_info=filter(lambda x: not x.tag_name.startswith('_'),
                            MPost2Label.get_by_uid(postinfo.uid).objects()),
            recent_apps=recent_apps,
            cat_enum=cat_enum1)

    def _the_view_kwd(self, postinfo):
        '''
        Generate the kwd dict for view.
        :param postinfo: the postinfo
        :return:  dict
        '''
        kwd = {
            'pager': '',
            'url': self.request.uri,
            'cookie_str': tools.get_uuid(),
            'daohangstr': '',
            'signature': postinfo.uid,
            'tdesc': '',
            'eval_0': MEvaluation.app_evaluation_count(postinfo.uid, 0),
            'eval_1': MEvaluation.app_evaluation_count(postinfo.uid, 1),
            'login': 1 if self.get_current_user() else 0,
            'has_image': 0,
            'parentlist': MCategory.get_parent_list(),
            'parentname': '',
            'catname': '',
            'router': router_post[postinfo.kind]
        }
        return kwd

    def fetch_additional_posts(self, uid):
        '''
        fetch the rel_recs, and random recs when view the post.
        '''
        cats = MPost2Catalog.query_by_entity_uid(uid, kind=self.kind)
        cat_uid_arr = []
        for cat_rec in cats:
            cat_uid = cat_rec.tag_id
            cat_uid_arr.append(cat_uid)
        logger.info('info category: {0}'.format(cat_uid_arr))
        rel_recs = MRelation.get_app_relations(uid, 8,
                                               kind=self.kind).objects()

        logger.info('rel_recs count: {0}'.format(rel_recs.count()))
        if cat_uid_arr:
            rand_recs = MPost.query_cat_random(cat_uid_arr[0],
                                               limit=4 - rel_recs.count() + 4)
        else:
            rand_recs = MPost.query_random(num=4 - rel_recs.count() + 4,
                                           kind=self.kind)
        return rand_recs, rel_recs

    def _add_relation(self, f_uid, t_uid):
        '''
        Add the relation. And the from and to, should have different weight.
        :param f_uid: the uid of `from` post.
        :param t_uid: the uid of `to` post.
        :return: return True if the relation has been succesfully added.
        '''
        if not MPost.get_by_uid(t_uid):
            return False
        if f_uid == t_uid:
            return False

        # 针对分类进行处理。只有落入相同分类的，才加1
        f_cats = MPost2Catalog.query_by_entity_uid(f_uid)
        t_cats = MPost2Catalog.query_by_entity_uid(t_uid)
        flag = False
        for f_cat in f_cats:
            for t_cat in t_cats:
                if f_cat.tag_id == t_cat.tag_id:
                    flag = True
        if flag:
            pass
        else:
            return False
        # 双向关联，但权重不一样.
        MRelation.add_relation(f_uid, t_uid, 2)
        MRelation.add_relation(t_uid, f_uid, 1)
        return True

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

        post_data['user_name'] = self.userinfo.user_name
        post_data['kind'] = self.kind

        # append external infor.

        if 'tags' in post_data:
            ext_dic['def_tag_arr'] = [
                x.strip()
                for x in post_data['tags'].strip().strip(',').split(',')
            ]
        ext_dic = dict(ext_dic, **self.ext_post_data(postdata=post_data))

        return (post_data, ext_dic)

    @tornado.web.authenticated
    @privilege.auth_add
    # @tornado.web.asynchronous
    @tornado.gen.coroutine
    def add(self, **kwargs):
        '''
        in infor.
        '''
        if 'uid' in kwargs:
            uid = kwargs['uid']
        else:
            uid = self._gen_uid()

        post_data, ext_dic = self.__parse_post_data()

        title = post_data['title'].strip()

        if len(title) < 2:
            kwd = {
                'info': 'Title cannot be less than 2 characters',
                'link': '/'
            }
            self.render('misc/html/404.html', userinfo=self.userinfo, kwd=kwd)

        if 'valid' in post_data:
            post_data['valid'] = int(post_data['valid'])
        else:
            post_data['valid'] = 1

        # 在应用中，会有分类的逻辑，需要处理
        if 'gcat0' in post_data:
            pass
        else:
            return False
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
        self.redirect('/{0}/{1}'.format(router_post[self.kind], uid))

    # @tornado.web.asynchronous
    @tornado.web.authenticated
    @privilege.auth_edit
    @tornado.gen.coroutine
    def update(self, uid):
        '''
        in infor.
        '''

        postinfo = MPost.get_by_uid(uid)
        if postinfo.kind == self.kind:
            pass
        else:
            return False

        post_data, ext_dic = self.__parse_post_data()
        if 'gcat0' in post_data:
            pass
        else:
            return False

        if 'valid' in post_data:
            post_data['valid'] = int(post_data['valid'])
        else:
            post_data['valid'] = postinfo.valid

        ext_dic['def_uid'] = uid
        # 用于判断是第几轮审核
        if postinfo.state[1] == '3':
            edit_count = int(postinfo.extinfo.get('def_edit_count', 0)) + 1
        else:
            edit_count = int(postinfo.extinfo.get('def_edit_count', 0))

        ext_dic['def_edit_count'] = edit_count
        # 用于记录审核通过后第几轮修改
        if postinfo.state[1] == '2':
            approved_count = int(postinfo.extinfo.get('def_approved_count', 0)) + 1
        else:
            approved_count = int(postinfo.extinfo.get('def_approved_count', 0))

        ext_dic['def_approved_count'] = approved_count

        cnt_old = tornado.escape.xhtml_unescape(postinfo.cnt_md).strip()
        cnt_new = post_data['cnt_md'].strip()
        if cnt_old == cnt_new:
            pass
        else:
            MPostHist.create_post_history(postinfo, self.userinfo)

        MPost.add_or_update_post(uid, post_data, extinfo=ext_dic)

        # todo:应该判断当前审核状态，是否可以进行修改状态。
        if postinfo.state[1] == '3':
            state_arr = ['a', 'b', 'c', 'd', 'e', 'f']
            if len(state_arr) > edit_count:
                pstate = str(state_arr[edit_count]) + '0' + postinfo.state[2:]

                MPost.update_state(uid, pstate)

        if postinfo.state[1] == '2':
            approved_state_arr = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
            if len(approved_state_arr) > approved_count:
                pstate = postinfo.state[0] + '1' + str(approved_state_arr[approved_count]) + '0'
            else:
                pstate = postinfo.state[0] + '190'
            MPost.update_state(uid, pstate)

        self._add_download_entity(ext_dic)
        # self.update_tag(uid=uid)

        update_category(uid, post_data)
        update_label(uid, post_data)
        # self.update_label(uid)

        logger.info('post kind:' + self.kind)
        # cele_gen_whoosh.delay()
        tornado.ioloop.IOLoop.instance().add_callback(self.cele_gen_whoosh)
        self.redirect('/{0}/{1}'.format(router_post[postinfo.kind], uid))

    @tornado.web.authenticated
    @privilege.auth_delete
    def _delete(self, *args, **kwargs):
        '''
        delete the post.
        '''
        _ = kwargs
        uid = args[0]
        current_infor = MPost.get_by_uid(uid)

        if MPost.delete(uid):

            tslug = MCategory.get_by_uid(current_infor.extinfo['def_cat_uid'])

            MCategory.update_count(current_infor.extinfo['def_cat_uid'])

            if router_post[self.kind] == 'info':
                url = "filter"
                id_dk8 = current_infor.extinfo['def_cat_uid']

            else:
                url = "list"
                id_dk8 = tslug.slug

            self.redirect('/{0}/{1}'.format(url, id_dk8))

        else:
            self.redirect('/{0}/{1}'.format(router_post[self.kind], uid))

    def _chuli_cookie_relation(self, app_id):
        '''
        The current Info and the Info viewed last should have some relation.
        And the last viewed Info could be found from cookie.
        '''
        last_app_uid = self.get_secure_cookie('use_app_uid')
        if last_app_uid:
            last_app_uid = last_app_uid.decode('utf-8')
        self.set_secure_cookie('use_app_uid', app_id)
        if last_app_uid and MPost.get_by_uid(last_app_uid):
            self._add_relation(last_app_uid, app_id)

    def ext_view_kwd(self, postinfo):
        '''
        The additional information. for View.
        '''
        _ = postinfo
        return {}

    def ext_tmpl_view(self, rec):
        '''
        Used for self defined templates. for View.
        '''
        return self._get_tmpl_view(rec)

    def ext_post_data(self, **kwargs):
        '''
        The additional information.  for add(), or update().
        '''
        _ = kwargs
        return {}

    def _add_download_entity(self, ext_dic):
        download_url = (ext_dic['tag_file_download'].strip().lower()
                        if ('tag_file_download' in ext_dic)
                        else '')
        the_entity = MEntity.get_id_by_impath(download_url)
        if the_entity:
            return True
        if download_url:
            MEntity.create_entity(path=download_url, desc=download_url, kind=4)

    @tornado.web.authenticated
    def _to_edit_kind(self, post_uid):
        '''
        Show the page for changing the category.
        '''
        if self.userinfo and self.userinfo.role[1] >= '3':
            pass
        else:
            self.redirect('/')
        postinfo = MPost.get_by_uid(post_uid, )
        json_cnt = json.dumps(postinfo.extinfo, indent=True)
        kwd = {}
        self.render('man_info/post_kind.html',
                    postinfo=postinfo,
                    sig_dic=router_post,
                    userinfo=self.userinfo,
                    json_cnt=json_cnt,
                    kwd=kwd)

    @tornado.web.authenticated
    @privilege.auth_edit
    def _change_kind(self, post_uid):
        '''
        To modify the category of the post, and kind.
        '''

        post_data = self.get_request_arguments()

        logger.info('admin post update: {0}'.format(post_data))

        MPost.update_misc(post_uid, kind=post_data['kcat'])
        # self.update_category(post_uid)

        update_category(post_uid, post_data)
        self.redirect('/{0}/{1}'.format(router_post[post_data['kcat']],
                                        post_uid))
