# -*- coding:utf-8 -*-

'''
The basic HTML Page handler.
'''

import json

import tornado.escape
import tornado.web
import random
from config import router_post
from torcms.core import tools
from torcms.core.base_handler import BaseHandler
from torcms.core.tools import logger
from torcms.model.category_model import MCategory
from torcms.model.label_model import MPost2Label
from torcms.model.post2catalog_model import MPost2Catalog
from torcms.model.post_hist_model import MPostHist
from torcms.model.post_model import MPost
from torcms.model.relation_model import MRelation
from torcms.model.evaluation_model import MEvaluation
from torcms.model.usage_model import MUsage

from celery_server import cele_gen_whoosh


class PostHandler(BaseHandler):
    '''
    The basic HTML Page handler.
    '''

    def initialize(self, **kwargs):
        super(PostHandler, self).initialize()

        if 'kind' in kwargs:
            self.kind = kwargs['kind']
        else:
            self.kind = '1'

        if 'filter_view' in kwargs:
            self.filter_view = True
        else:
            self.filter_view = False

    def get(self, *args):

        url_str = args[0]
        url_arr = self.parse_url(url_str)

        if url_str == '':
            self.index()
        elif url_str == 'recent':
            # Deprecated
            self.redirect('/post_list/recent')
        elif url_str == '_refresh':
            # Deprecated
            self.redirect('/post_list/_refresh')
        elif len(url_arr) == 1 and url_str.endswith('.html'):
            # Deprecated
            self.view_or_add(url_str.split('.')[0])
        elif url_arr[0] in ['_cat_add', 'cat_add']:
            self.to_add(catid=url_arr[1])
        elif url_arr[0] in ['_add', 'add_document', 'add']:
            # self.to_add()
            if len(url_arr) == 2:
                self.to_add(uid=url_arr[1])
            else:
                self.to_add()
        elif url_arr[0] in ['modify', 'edit', '_edit']:
            self.to_edit(url_arr[1])
        elif url_arr[0] == 'delete':
            self.delete(url_arr[1])
        elif url_arr[0] == 'j_delete':
            self.j_delete(url_arr[1])
        elif url_arr[0] in ['j_count_plus', 'ajax_count_plus', ]:
            self.j_count_plus(url_arr[1])
        elif len(url_arr) == 1:
            if len(url_str) in [4, 5]:
                self.view_or_add(url_str)
                # self.view_or_add(url_str)

        else:
            kwd = {
                'title': '',
                'info': '404. Page not found!',
            }
            self.set_status(404)
            self.render('html/404.html', kwd=kwd,
                        userinfo=self.userinfo, )

    def post(self, *args):
        url_str = args[0]
        logger.info('Post url: {0}'.format(url_str))

        url_arr = self.parse_url(url_str)

        if url_arr[0] in ['_edit', 'edit', 'modify']:
            self.update(url_arr[1])
        elif url_arr[0] in ['_add', 'add', 'add_document', ]:
            if len(url_arr) == 2:
                self.add(uid=url_arr[1])
            else:
                self.add()
        elif url_arr[0] in ['_cat_add', 'cat_add']:
            self.add(catid=url_arr[1])
        elif len(url_arr) == 1:
            # Todo: should not exists.
            if len(url_str) in [4, 5]:
                self.add(uid=url_str)
        elif url_arr[0] == 'rel' and len(url_arr) == 3:
            self.add_relation(url_arr[1], url_arr[2])
        else:

            kwd = {
                'title': '',
                'info': '404. No such action!',
            }
            self.set_status(404)
            self.render('html/404.html', kwd=kwd,
                        userinfo=self.userinfo, )

    def index(self):
        '''
        The default page of POST.
        :return:
        '''
        self.render('post_{0}/index.html'.format(self.kind),
                    userinfo=self.userinfo,
                    kwd={'uid': '',})

    def j_count_plus(self, uid):
        '''
        Ajax request, that the view count will plus 1.
        :param uid:
        :return:
        '''
        logger.info('Deprecated, you should use: /post_j/count_plus')
        self.set_header("Content-Type", "application/json")
        output = {
            'status': 1 if MPost.update_view_count_by_uid(uid) else 0,
        }
        self.write(json.dumps(output))

    @tornado.web.authenticated
    def __could_edit(self, postid):
        post_rec = MPost.get_by_uid(postid)
        if post_rec:
            pass
        else:
            return False
        if self.check_post_role()['EDIT']:
            return True
        elif post_rec.user_name == self.userinfo.user_name:
            return True
        else:
            return False

    def view_or_add(self, uid):
        '''
        Try to get the post. If not, to add the wiki.
        :param uid:
        :return:
        '''
        postinfo = MPost.get_by_uid(uid)
        if postinfo:
            self.viewinfo(postinfo)
        elif self.userinfo:
            self.to_add(uid=uid)
        else:
            kwd = {
                'info': '404. Page not found!',
            }
            self.render('html/404.html', kwd=kwd,
                        userinfo=self.userinfo, )

    # @tornado.web.authenticated
    # def to_add(self, **args):
    #     # uid = args[0]
    #     if self.check_post_role()['ADD']:
    #         pass
    #     else:
    #         return False
    #     kwd = {
    #         'pager': '',
    #         'cats': MCategory.query_all(),
    #         'uid': '',
    #     }
    #     self.render('post_{0}/post_add.html'.format(self.kind),
    #                 kwd=kwd,
    #                 tag_infos=MCategory.query_all(),
    #                 userinfo=self.userinfo,
    #                 cfg=CMS_CFG, )

    @tornado.web.authenticated
    def to_add(self, **kwargs):
        '''
        Used for info1.
        '''

        if 'catid' in kwargs:
            catid = kwargs['catid']
            return self.__to_add_with_category(catid)

        else:

            if self.check_post_role()['ADD']:
                pass
            else:
                return False

            if 'uid' in kwargs and MPost.get_by_uid(kwargs['uid']):
                # todo:
                # self.redirect('/{0}/edit/{1}'.format(self.app_url_name, uid))
                uid = kwargs['uid']
            else:
                uid = ''
            self.render('post_{0}/add.html'.format(self.kind),
                        tag_infos=MCategory.query_all(by_order=True, kind=self.kind),
                        userinfo=self.userinfo,
                        kwd={'uid': uid,})

    # In Post
    # @tornado.web.authenticated
    # def update(self, uid):
    #     '''
    #     Update the post according to the uid.
    #     :param uid:
    #     :return:
    #     '''
    #     if self.__could_edit(uid):
    #         pass
    #     else:
    #         return False
    #
    #     postinfo = MPost.get_by_uid(uid)
    #     if postinfo.kind == self.kind:
    #         pass
    #     else:
    #         return False
    #
    #     post_data = self.get_post_data()
    #
    #     post_data['user_name'] = self.get_current_user()
    #     post_data['kind'] = self.kind
    #     is_update_time = True if post_data['is_update_time'][0] == '1' else False
    #
    #     cnt_old = tornado.escape.xhtml_unescape(postinfo.cnt_md).strip()
    #     cnt_new = post_data['cnt_md'].strip()
    #     if cnt_old == cnt_new:
    #         pass
    #     else:
    #         MPostHist.create_wiki_history(postinfo)
    #
    #     logger.info('upadte: {0}'.format(uid))
    #     logger.info('Update post_data: {0}'.format(post_data))
    #     MPost.update(uid, post_data, update_time=is_update_time)
    #     self.update_category(uid)
    #     self.update_tag(uid)
    #
    #     cele_gen_whoosh.delay()
    #     # run_whoosh.run()
    #     self.redirect('/{0}/{1}'.format(router_post[postinfo.kind], uid))

    @tornado.web.authenticated
    @tornado.web.asynchronous
    def update(self, uid):
        '''
        in infor.
        :param uid:
        :return:
        '''
        if self.check_post_role()['EDIT']:
            pass
        else:
            return False

        postinfo = MPost.get_by_uid(uid)
        if postinfo.kind == self.kind:
            pass
        else:
            return False

        post_data = {}
        ext_dic = {}
        for key in self.request.arguments:
            if key.startswith('ext_') or key.startswith('tag_'):
                ext_dic[key] = self.get_argument(key)
            else:
                post_data[key] = self.get_arguments(key)[0]

        post_data['user_name'] = self.userinfo.user_name

        if 'valid' in post_data:
            post_data['valid'] = int(post_data['valid'])
        else:
            post_data['valid'] = postinfo.valid

        ext_dic['def_uid'] = str(uid)
        logger.info(post_data)

        ext_dic = dict(ext_dic, **self.get_extra_data(postdata=post_data))

        cnt_old = tornado.escape.xhtml_unescape(postinfo.cnt_md).strip()
        cnt_new = post_data['cnt_md'].strip()
        if cnt_old == cnt_new:
            pass
        else:
            MPostHist.create_wiki_history(postinfo)

        MPost.modify_meta(uid,
                          post_data,
                          extinfo=ext_dic)
        self.update_category(uid)
        self.update_tag(uid)

        logger.info('post kind:' + self.kind)
        logger.info('update jump to:', '/{0}/{1}'.format(router_post[self.kind], uid))
        cele_gen_whoosh.delay()
        # run_whoosh.run()
        self.redirect('/{0}/{1}'.format(router_post[postinfo.kind], uid))

    @tornado.web.authenticated
    def update_tag(self, signature):
        '''
        Update the tags when updating.
        :param signature:
        :return:
        '''
        current_tag_infos = MPost2Label.get_by_uid(signature, kind=self.kind)
        post_data = self.get_post_data()
        if 'tags' in post_data:
            pass
        else:
            return False

        print('tags: {0}'.format(post_data['tags']))
        tags_arr = [x.strip() for x in post_data['tags'].split(',')]
        for tag_name in tags_arr:
            if tag_name == '':
                pass
            else:
                MPost2Label.add_record(signature, tag_name, 1)

        for cur_info in current_tag_infos:
            print(cur_info.tag.name)
            if cur_info.tag.name in tags_arr:
                pass
            else:
                MPost2Label.remove_relation(signature, cur_info.tag)

    @tornado.web.authenticated
    def update_category(self, uid):
        '''
        Update the category of the post.
        :param uid:  The ID of the post. Extra info would get by requests.
        :return:
        '''
        post_data = self.get_post_data()

        current_infos = MPost2Catalog.query_by_entity_uid(uid)
        new_tag_arr = []
        def_cate_arr = ['gcat{0}'.format(x) for x in range(10)]
        # todo: next line should be deleted. keep here for historical reason.
        def_cate_arr.append('def_cat_uid')

        for key in def_cate_arr:
            if key in post_data:
                pass
            else:
                continue

            if post_data[key] == '' or post_data[key] == '0':
                continue

            # 有可能选重复了。保留前面的
            if post_data[key] in new_tag_arr:
                continue

            new_tag_arr.append(post_data[key] + ' ' * (4 - len(post_data[key])))

        # Add the category
        for index, catid in enumerate(new_tag_arr):
            MPost2Catalog.add_record(uid, catid, index)

            # MCategory.update_count(catid, MPost2Catalog.query_by_catid(catid).count())

        # Delete the old category if not in post requests.
        for cur_info in current_infos:
            if str(cur_info.tag.uid).strip() not in new_tag_arr:
                MPost2Catalog.remove_relation(uid, cur_info.tag)

    # in post.
    # @tornado.web.authenticated
    # def to_edit(self, uid):
    #     '''
    #     Show the HTML page for editing the post.
    #     :param uid:
    #     :return:
    #     '''
    #     if self.__could_edit(uid):
    #         pass
    #     else:
    #         return False
    #
    #     kwd = {
    #         'pager': '',
    #         'cats': MCategory.query_all(),
    #
    #     }
    #     postinfo = MPost.get_by_uid(uid)
    #     self.render('post_{0}/post_edit.html'.format(self.kind),
    #                 kwd=kwd,
    #                 unescape=tornado.escape.xhtml_unescape,
    #                 tag_infos=MCategory.query_all(kind=self.kind),
    #                 app2label_info=MPost2Label.get_by_uid(uid),
    #                 app2tag_info=MPost2Catalog.query_by_entity_uid(uid, self.kind),
    #                 dbrec=postinfo,
    #                 postinfo=postinfo,
    #                 userinfo=self.userinfo,
    #                 cfg=CMS_CFG, )

    @tornado.web.authenticated
    def to_edit(self, infoid):
        '''
        in infor
        :param infoid:
        :return:
        '''
        if self.check_post_role()['EDIT']:
            pass
        else:
            return False

        rec_info = MPost.get_by_uid(infoid)
        postinfo = rec_info

        if rec_info:
            pass
        else:
            self.render('html/404.html')
            return
        if 'def_cat_uid' in rec_info.extinfo:
            catid = rec_info.extinfo['def_cat_uid']
        else:
            catid = ''

        if len(catid) == 4:
            pass
        else:
            catid = ''

        catinfo = None
        p_catinfo = None

        post2catinfo = MPost2Catalog.get_entry_catalog(postinfo.uid)
        if post2catinfo:
            catid = post2catinfo.tag.uid
            catinfo = MCategory.get_by_uid(catid)
            if catinfo:
                p_catinfo = MCategory.get_by_uid(catinfo.pid)

        kwd = {
            'def_cat_uid': catid,
            'parentname': '',
            'catname': '',
            'parentlist': MCategory.get_parent_list(),
            'userip': self.request.remote_ip}

        if self.filter_view:
            tmpl = 'autogen/edit/edit_{0}.html'.format(catid)
        else:
            tmpl = 'post_{0}/edit.html'.format(self.kind)

        logger.info('Meta template: {0}'.format(tmpl))

        self.render(tmpl,
                    kwd=kwd,
                    calc_info=rec_info,  # Deprecated
                    post_info=rec_info,  # Deprecated
                    app_info=rec_info,  # Deprecated
                    postinfo=rec_info,
                    catinfo=catinfo,
                    pcatinfo=p_catinfo,
                    userinfo=self.userinfo,
                    unescape=tornado.escape.xhtml_unescape,
                    cat_enum=MCategory.get_qian2(catid[:2]),
                    tag_infos=MCategory.query_all(by_order=True, kind=self.kind),
                    tag_infos2=MCategory.query_all(by_order=True, kind=self.kind),
                    app2tag_info=MPost2Catalog.query_by_entity_uid(infoid, kind=self.kind),
                    app2label_info=MPost2Label.get_by_uid(infoid, kind=self.kind + '1'))

    def __gen_last_current_relation(self, post_id):
        '''
        Generate the relation for the post and last post viewed.
        :param post_id:
        :return:
        '''
        last_post_id = self.get_secure_cookie('last_post_uid')
        if last_post_id:
            last_post_id = last_post_id.decode('utf-8')
        self.set_secure_cookie('last_post_uid', post_id)

        if last_post_id and MPost.get_by_uid(last_post_id):
            self.add_relation(last_post_id, post_id)

    # def viewinfo(self, postinfo):
    #     logger.info('View infor, uid: {uid}, kind: {kind}, title: {title}'.format(
    #         kind=postinfo.kind,
    #         uid=postinfo.uid,
    #         title=postinfo.title
    #     ))
    #     post_id = postinfo.uid
    #     self.__gen_last_current_relation(post_id)
    #     cats = MPost2Catalog.query_by_entity_uid(post_id)
    #     tag_info = MPost2Label.get_by_uid(post_id)
    #     if postinfo.kind == self.kind:
    #         pass
    #     else:
    #         self.redirect('/{0}/{1}'.format(router_post[postinfo.kind], post_id), permanent=True)
    #
    #     if not postinfo:
    #         kwd = {
    #             'info': '您要查看的页面不存在。',
    #         }
    #         self.render('html/404.html',
    #                     kwd=kwd,
    #                     userinfo=self.userinfo)
    #         return False
    #
    #     if cats.count() == 0:
    #         cat_id = ''
    #     else:
    #         cat_id = cats.get().tag
    #     kwd = {
    #         'pager': '',
    #         'editable': self.editable(),
    #         'cat_id': cat_id
    #     }
    #
    #     rel_recs = MRelation.get_app_relations(postinfo.uid, 4)
    #     rand_recs = MPost.query_random(num=4 - rel_recs.count() + 2, kind=self.kind)
    #
    #     self.render('post_{0}/post_view.html'.format(self.kind),
    #                 view=postinfo,
    #                 postinfo=postinfo,
    #                 unescape=tornado.escape.xhtml_unescape,
    #                 kwd=kwd,
    #                 userinfo=self.userinfo,
    #                 tag_info=tag_info,
    #                 relations=rel_recs,
    #                 rand_recs=rand_recs,
    #                 replys=[],
    #                 cfg=CMS_CFG, )

    def viewinfo(self, postinfo):
        '''
        In infor.
        :param postinfo:
        :return:
        '''
        info_id = postinfo.uid

        logger.warning('info kind:{0} '.format(postinfo.kind))

        # If not, there must be something wrong.
        if postinfo.kind == self.kind:
            pass
        else:
            self.redirect('/{0}/{1}'.format(router_post[postinfo.kind], info_id), permanent=True)

        if postinfo:
            pass
        else:
            kwd = {
                'info': '您要找的信息不存在。',
            }
            self.render('html/404.html',
                        kwd=kwd,
                        userinfo=self.userinfo, )
            return False

        cats = MPost2Catalog.query_by_entity_uid(info_id, kind=postinfo.kind)
        cat_uid_arr = []
        for cat_rec in cats:
            cat_uid = cat_rec.tag.uid
            cat_uid_arr.append(cat_uid)
        logger.info('info category: {0}'.format(cat_uid_arr))

        rel_recs = MRelation.get_app_relations(postinfo.uid, 8, kind=postinfo.kind)
        logger.info('rel_recs count: {0}'.format(rel_recs.count()))

        if len(cat_uid_arr) > 0:
            rand_recs = MPost.query_cat_random(cat_uid_arr[0], 4 - rel_recs.count() + 4)
        else:
            rand_recs = MPost.query_random(num=4 - rel_recs.count() + 4, kind=postinfo.kind)

        self.chuli_cookie_relation(info_id)
        cookie_str = tools.get_uuid()

        if 'def_cat_uid' in postinfo.extinfo:
            ext_catid = postinfo.extinfo['def_cat_uid']
            if ext_catid:
                pass
            else:
                ext_catid = ''
        else:
            ext_catid = ''

        if len(ext_catid) == 4:
            pass
        else:
            ext_catid = ''

        catinfo = None
        p_catinfo = None

        post2catinfo = MPost2Catalog.get_entry_catalog(postinfo.uid)
        if post2catinfo:
            catid = post2catinfo.tag.uid
            catinfo = MCategory.get_by_uid(catid)
            if catinfo:
                p_catinfo = MCategory.get_by_uid(catinfo.pid)

        kwd = {
            'pager': '',
            'url': self.request.uri,
            'cookie_str': cookie_str,
            'daohangstr': '',
            'signature': info_id,
            'tdesc': '',
            'eval_0': MEvaluation.app_evaluation_count(info_id, 0),
            'eval_1': MEvaluation.app_evaluation_count(info_id, 1),
            'login': 1 if self.get_current_user() else 0,
            'has_image': 0,
            'parentlist': MCategory.get_parent_list(),
            'parentname': '',
            'catname': '',
            'router': router_post[postinfo.kind]
        }
        MPost.view_count_increase(info_id)
        if self.get_current_user():
            MUsage.add_or_update(self.userinfo.uid, info_id, postinfo.kind)
        self.set_cookie('user_pass', cookie_str)
        # tmpl = self.get_tmpl_name(postinfo)

        tmpl = self.ext_tmpl_view(postinfo)

        ext_catid2 = postinfo.extinfo['def_cat_uid'] if 'def_cat_uid' in postinfo.extinfo else None

        if self.userinfo:
            recent_apps = MUsage.query_recent(self.userinfo.uid, postinfo.kind, 6)[1:]
        else:
            recent_apps = []
        logger.info('The Info Template: {0}'.format(tmpl))
        self.render(tmpl,
                    kwd=dict(kwd, **self.ext_view_kwd(postinfo)),
                    postinfo=postinfo,
                    calc_info=postinfo,  # Deprecated
                    post_info=postinfo,  # Deprecated
                    userinfo=self.userinfo,
                    catinfo=catinfo,
                    pcatinfo=p_catinfo,
                    relations=rel_recs,
                    rand_recs=rand_recs,
                    unescape=tornado.escape.xhtml_unescape,
                    ad_switch=random.randint(1, 18),
                    tag_info=MPost2Label.get_by_uid(info_id),
                    recent_apps=recent_apps,
                    cat_enum=MCategory.get_qian2(ext_catid2[:2]) if ext_catid else [], )

    # def add_relation(self, f_uid, t_uid):
    #     if MPost.get_by_uid(t_uid) is False:
    #         return False
    #     if f_uid == t_uid:  # relate to itself.
    #         return False
    #
    #     MRelation.add_relation(f_uid, t_uid, 2)
    #     MRelation.add_relation(t_uid, f_uid, 1)
    #     return True

    def add_relation(self, f_uid, t_uid):
        '''
        Add the relation. And the from and to, should have different weight.
        :param f_uid:
        :param t_uid:
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
                if f_cat.tag == t_cat.tag:
                    flag = True
        if flag:
            pass
        else:
            return False
        # 双向关联，但权重不一样.
        MRelation.add_relation(f_uid, t_uid, 2)
        MRelation.add_relation(t_uid, f_uid, 1)
        return True

    # In Post.
    # @tornado.web.authenticated
    # @tornado.web.asynchronous
    # def add(self, **kwargs):
    #
    #     if 'uid' in kwargs:
    #         uid = kwargs['uid']
    #     else:
    #         uid = self.__gen_uid()
    #     if self.check_post_role()['ADD']:
    #         pass
    #     else:
    #         return False
    #     post_data = self.get_post_data()
    #     if 'title' in post_data:
    #         pass
    #     else:
    #         self.set_status(400)
    #         return False
    #
    #     post_data['user_name'] = self.userinfo.user_name
    #     post_data['kind'] = self.kind
    #     cur_post_rec = MPost.get_by_uid(uid)
    #     if cur_post_rec:
    #         pass
    #     else:
    #         if MPost.create_wiki_history(uid, post_data):
    #             self.update_tag(uid)
    #             self.update_category(uid)
    #     # run_whoosh.run()
    #     cele_gen_whoosh.delay()
    #     self.redirect('/{0}/{1}'.format(router_post[self.kind], uid))

    @tornado.web.authenticated
    @tornado.web.asynchronous
    def add(self, **kwargs):
        '''
        in infor.
        :param kwargs:
        :return:
        '''
        if 'uid' in kwargs:
            uid = kwargs['uid']
        else:
            uid = self.__gen_uid()

        if self.check_post_role()['ADD']:
            pass
        else:
            return False

        ext_dic = {}
        post_data = {}
        for key in self.request.arguments:
            if key.startswith('ext_') or key.startswith('tag_'):
                ext_dic[key] = self.get_argument(key)
            else:
                post_data[key] = self.get_arguments(key)[0]
        post_data['user_name'] = self.userinfo.user_name

        post_data['kind'] = self.kind

        if 'catid' in kwargs:
            catid = kwargs['catid']

            catinfo = MCategory.get_by_uid(catid)
            if catinfo:
                post_data['kind'] = catinfo.kind
                logger.info('Got category inf: {0} , kind: {1}'.format(catinfo.name, catinfo.kind))
            else:
                logger.info('Could not find the category: {0}'.format(catid))
        else:
            catid = ''

        logger.info('info adding: ', 'catid: ', catid, 'infoid:', uid)

        if 'valid' in post_data:
            post_data['valid'] = int(post_data['valid'])
        else:
            post_data['valid'] = 1

        ext_dic['def_uid'] = uid

        ext_dic = dict(ext_dic, **self.get_extra_data(postdata=post_data))

        MPost.modify_meta(ext_dic['def_uid'],
                          post_data,
                          extinfo=ext_dic)
        self.update_category(ext_dic['def_uid'])
        self.update_tag(ext_dic['def_uid'])

        cele_gen_whoosh.delay()

        self.redirect('/{0}/{1}'.format(router_post[self.kind], uid))

    # def __gen_uid(self):
    #
    #     new_uid = tools.get_uu5d()
    #     while MPost.get_by_uid(new_uid):
    #         new_uid = tools.get_uu5d()
    #     return new_uid

    def __gen_uid(self):
        '''
        Generate the ID for post.
        :return: the new ID.
        '''
        cur_uid = self.kind + tools.get_uu4d()
        while MPost.get_by_uid(cur_uid):
            cur_uid = self.kind + tools.get_uu4d()
        return cur_uid

    @tornado.web.authenticated
    def delete(self, *args, **kwargs):
        uid = args[0]
        current_infor = MPost.get_by_uid(uid)

        if self.check_post_role()['DELETE']:
            pass
        else:
            return False

        if MPost.delete(uid):
            self.redirect('/list/{0}'.format(current_infor.extinfo['def_cat_uid']))
        else:
            self.redirect('/{0}/{1}'.format(router_post[self.kind], uid))

    @tornado.web.authenticated
    def j_delete(self, uid):
        '''
        Delete the post, but return the JSON.
        :param uid:
        :return:
        '''
        logger.info('Deprecated, you should use: /post_j/delete')

        if self.check_post_role()['DELETE']:
            pass
        else:
            return False
        is_deleted = MPost.delete(uid)

        if is_deleted:
            output = {
                'del_info ': 1,
            }
        else:
            output = {
                'del_info ': 0,
            }
        return json.dump(output, self)

    def ext_view_kwd(self, info_rec):
        '''
        The additional information.
        :param info_rec:
        :return: directory.
        '''
        return {}

    def ext_tmpl_view(self, rec):
        '''
        Used for self defined templates.
        :param rec:
        :return:
        '''
        return self.__get_tmpl_view(rec)

    def ext_post_data(self, **kwargs):
        '''
        The additional information.
        :param post_data:
        :return: directory.
        '''
        return {}

    def chuli_cookie_relation(self, app_id):
        '''
        The current Info and the Info viewed last should have some relation.
        And the last viewed Info could be found from cookie.
        :param app_id: the current app
        :return: None
        '''
        last_app_uid = self.get_secure_cookie('use_app_uid')
        if last_app_uid:
            last_app_uid = last_app_uid.decode('utf-8')
        self.set_secure_cookie('use_app_uid', app_id)
        if last_app_uid and MPost.get_by_uid(last_app_uid):
            self.add_relation(last_app_uid, app_id)

    # def _is_tpl2(self):
    #     if 'tpl2' in CMS_CFG and self.kind in CMS_CFG['tpl2']:
    #         return True
    #     return False

    def __get_tmpl_view(self, rec):
        '''
        According to the application, each info of it's classification could has different temaplate.
        :param rec: the App record.
        :return: the temaplte path.
        '''
        if 'def_cat_uid' in rec.extinfo and rec.extinfo['def_cat_uid'] != '':
            cat_id = rec.extinfo['def_cat_uid']
        else:
            cat_id = False
        if cat_id and self.filter_view:
            tmpl = 'autogen/view/view_{0}.html'.format(cat_id)
        else:
            tmpl = 'post_{0}/post_view.html'.format(self.kind)
        return tmpl

    @tornado.web.authenticated
    def __to_add_with_category(self, catid):
        '''
        Used for info2.
        :param catid: the uid of category
        :return:
        '''
        if self.check_post_role()['ADD']:
            pass
        else:
            return False
        catinfo = MCategory.get_by_uid(catid)
        kwd = {
            'uid': self.__gen_uid(),
            'userid': self.userinfo.user_name if self.userinfo else '',
            'def_cat_uid': catid,
            'parentname': MCategory.get_by_uid(catinfo.pid).name,
            'catname': MCategory.get_by_uid(catid).name,
        }

        self.render('autogen/add/add_{0}.html'.format(catid),
                    userinfo=self.userinfo,
                    kwd=kwd)

    def get_extra_data(self, **kwargs):
        '''
        得到预定义的额外信息
        '''
        postdata = kwargs['postdata']
        logger.info('Def Extra data: args - {0}'.format(postdata))

        ext_data = {}
        # 针对分类下面两种处理方式，上面是原有的，暂时保留以保持兼容
        if 'def_cat_uid' in postdata:
            ext_data['def_cat_uid'] = postdata['def_cat_uid']
            ext_data['def_cat_pid'] = MCategory.get_by_uid(postdata['def_cat_uid']).pid
        if 'gcat0' in postdata:
            ext_data['def_cat_uid'] = postdata['gcat0']
            ext_data['def_cat_pid'] = MCategory.get_by_uid(postdata['gcat0']).pid

        ext_data['def_tag_arr'] = [x.strip() for x in postdata['tags'].strip().strip(',').split(',')]

        ext_data = dict(ext_data, **self.ext_post_data(postdata=postdata))

        return ext_data
