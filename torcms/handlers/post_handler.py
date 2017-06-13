# -*- coding:utf-8 -*-

'''
The basic HTML Page handler.
'''

import json
import random
from concurrent.futures import ThreadPoolExecutor
import tornado.escape
import tornado.web
import tornado.ioloop
from torcms.core import tools
from torcms.core.base_handler import BaseHandler
from torcms.core.tools import logger
from torcms.core.libs.deprecation import deprecated
from torcms.model.category_model import MCategory
from torcms.model.label_model import MPost2Label
from torcms.model.post2catalog_model import MPost2Catalog
from torcms.model.post_hist_model import MPostHist
from torcms.model.post_model import MPost
from torcms.model.relation_model import MRelation
from torcms.model.evaluation_model import MEvaluation
from torcms.model.usage_model import MUsage
from config import router_post, DB_CFG


class PostHandler(BaseHandler):
    '''
    The basic HTML Page handler.
    '''
    executor = ThreadPoolExecutor(2)

    def initialize(self, **kwargs):
        super(PostHandler, self).initialize()

        if 'kind' in kwargs:
            self.kind = kwargs['kind']
        else:
            self.kind = '1'

        self.filter_view = kwargs['filter_view'] if 'filter_view' in kwargs else False

    def _redirect(self, url_arr):
        '''
        Redirection.
        :param url_arr:
        :return:
        '''
        direct_dic = {
            'recent': '/post_list/recent',
            'refresh': '/post_list/_refresh',
            '_refresh': '/post_list/_refresh',

        }
        sig = url_arr[0]
        for sig_enum in direct_dic:
            if sig == sig_enum:
                self.redirect(direct_dic[sig])
        pre_dic = {
            'cat_add': '_cat_add',
            'add_document': '_add',
            'add': '_add',
            'modify': '_edit',
            'edit': '_edit',
            'delete': '_delete',
            'ajax_count_plus': 'j_count_plus',
        }
        sig = url_arr[0]
        for sig_enum in pre_dic:
            if sig == sig_enum:
                url_arr = [pre_dic[sig_enum]] + url_arr[1:]
                url_str = '/post/' + '/'.join(url_arr)
                self.redirect(url_str)
        return True

    def get(self, *args):

        url_str = args[0]
        url_arr = self.parse_url(url_str)
        if len(url_arr) > 0:
            self._redirect(url_arr)

        if url_str == '':
            self.index()
        elif url_arr[0] == '_cat_add':
            self._to_add(catid=url_arr[1])
        elif url_arr[0] == '_add':
            if len(url_arr) == 2:
                self._to_add(uid=url_arr[1])
            else:
                self._to_add()
        elif url_arr[0] == '_edit_kind':
            self._to_edit_kind(url_arr[1])
        elif url_arr[0] == '_edit':
            self._to_edit(url_arr[1])
        elif url_arr[0] == '_delete':
            self.delete(url_arr[1])
        elif url_arr[0] == 'j_delete':
            self.j_delete(url_arr[1])
        elif url_arr[0] == 'j_count_plus':
            self.j_count_plus(url_arr[1])
        elif len(url_arr) == 1 and url_str.endswith('.html'):
            # Deprecated
            self.redirect('/post/{uid}'.format(uid=url_str.split('.')[0]))
        elif len(url_arr) == 1 and len(url_str) in [4, 5]:
            self.view_or_add(url_str)
        else:
            kwd = {
                'title': '',
                'info': '404. Page not found!',
            }
            self.set_status(404)
            self.render('misc/html/404.html', kwd=kwd,
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
        elif url_arr[0] == '_edit_kind':
            self._change_kind(url_arr[1])
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
            self.render('misc/html/404.html', kwd=kwd,
                        userinfo=self.userinfo, )

    def index(self):
        '''
        The default page of POST.
        :return:
        '''
        self.render('post_{0}/post_index.html'.format(self.kind),
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

    @tornado.web.authenticated
    def _could_edit(self, postid):
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

    def _get_tmpl_view(self, rec):
        '''
        According to the application, each info of it's classification could
        has different temaplate.
        :param rec: the App record.
        :return: the temaplte path.
        '''

        if 'gcat0' in rec.extinfo and rec.extinfo['gcat0'] != '':
            cat_id = rec.extinfo['gcat0']
        elif 'def_cat_uid' in rec.extinfo and rec.extinfo['def_cat_uid'] != '':
            cat_id = rec.extinfo['def_cat_uid']
        else:
            cat_id = None

        logger.info('For templates: catid: {0},  filter_view: {1}'.format(cat_id, self.filter_view))

        if cat_id and self.filter_view:
            tmpl = 'autogen/view/view_{0}.html'.format(cat_id)
        else:
            tmpl = 'post_{0}/post_view.html'.format(self.kind)
        return tmpl

    @tornado.web.authenticated
    def _to_add_with_category(self, catid):
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
            'uid': self._gen_uid(),
            'userid': self.userinfo.user_name if self.userinfo else '',
            'def_cat_uid': catid,
            'parentname': MCategory.get_by_uid(catinfo.pid).name,
            'catname': MCategory.get_by_uid(catid).name,
        }

        self.render('autogen/add/add_{0}.html'.format(catid),
                    userinfo=self.userinfo,
                    kwd=kwd)

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
            self._to_add(uid=uid)
        else:
            kwd = {
                'info': '404. Page not found!',
            }
            self.render('misc/html/404.html', kwd=kwd,
                        userinfo=self.userinfo, )

    @tornado.web.authenticated
    def _to_add(self, **kwargs):
        '''
        Used for info1.
        '''

        if 'catid' in kwargs:
            catid = kwargs['catid']
            return self._to_add_with_category(catid)

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
            self.render('post_{0}/post_add.html'.format(self.kind),
                        tag_infos=MCategory.query_all(by_order=True, kind=self.kind),
                        userinfo=self.userinfo,
                        kwd={'uid': uid, })

    def update_tag(self, uid='', **kwargs):
        '''
        Update category, and labels.
        :param uid:
        :param kwargs:
        :return:
        '''
        self.update_category(uid, **kwargs)
        self.update_label(uid)

    @tornado.web.authenticated
    def update_label(self, signature):
        '''
        Update the label when updating.
        :param signature:
        :return:
        '''
        current_tag_infos = MPost2Label.get_by_uid(signature, kind=self.kind).naive()
        post_data = self.get_post_data()
        if 'tags' in post_data:
            pass
        else:
            return False

        tags_arr = [x.strip() for x in post_data['tags'].split(',')]
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

    @tornado.web.authenticated
    def update_category(self, uid, **kwargs):
        '''
        Update the category of the post.
        :param uid:  The ID of the post. Extra info would get by requests.
        :return:
        '''

        catid = kwargs['catid'] if ('catid' in kwargs
                                    and MCategory.get_by_uid(kwargs['catid'])) else None

        post_data = self.get_post_data()

        current_infos = MPost2Catalog.query_by_entity_uid(uid, kind=self.kind).naive()

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
        elif len(new_category_arr) > 0:
            def_cat_id = new_category_arr[0]
        else:
            def_cat_id = None

        if def_cat_id:
            cat_dic['def_cat_uid'] = def_cat_id
            cat_dic['def_cat_pid'] = MCategory.get_by_uid(def_cat_id).pid

        # Add the category
        logger.info('Update category: {0}'.format(new_category_arr))
        logger.info('Update category: {0}'.format(cat_dic))

        MPost.update_jsonb(uid, cat_dic)

        for index, catid in enumerate(new_category_arr):
            MPost2Catalog.add_record(uid, catid, index)

        # Delete the old category if not in post requests.
        for cur_info in current_infos:
            if cur_info.tag_id not in new_category_arr:
                MPost2Catalog.remove_relation(uid, cur_info.tag_id)

    @tornado.web.authenticated
    def _to_edit(self, infoid):
        '''
        render the HTML page for post editing.
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
            self.render('misc/html/404.html')
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

        post2catinfo = MPost2Catalog.get_first_category(postinfo.uid)
        if post2catinfo:
            catid = post2catinfo.tag_id
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
            tmpl = 'post_{0}/post_edit.html'.format(self.kind)

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
                    app2tag_info=MPost2Catalog.query_by_entity_uid(infoid, kind=self.kind).naive(),
                    app2label_info=MPost2Label.get_by_uid(infoid, kind=self.kind + '1').naive())

    def _gen_last_current_relation(self, post_id):
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

    def viewinfo(self, postinfo):
        '''
        In infor.
        :param postinfo:
        :return:
        '''
        logger.warning('info kind:{0} '.format(postinfo.kind))

        # If not, there must be something wrong.
        if postinfo.kind == self.kind:
            pass
        else:
            self.redirect('/{0}/{1}'.format(router_post[postinfo.kind], postinfo.uid),
                          permanent=True)

        ext_catid = postinfo.extinfo['def_cat_uid'] if 'def_cat_uid' in postinfo.extinfo else ''
        ext_catid2 = postinfo.extinfo['def_cat_uid'] if 'def_cat_uid' in postinfo.extinfo else None
        cat_enum1 = MCategory.get_qian2(ext_catid2[:2]) if ext_catid else []

        rand_recs, rel_recs = self.fetch_additional_posts(postinfo.uid)

        self._chuli_cookie_relation(postinfo.uid)
        cookie_str = tools.get_uuid()

        catinfo = None
        p_catinfo = None

        post2catinfo = MPost2Catalog.get_first_category(postinfo.uid)
        if post2catinfo:
            catinfo = MCategory.get_by_uid(post2catinfo.tag_id)
            if catinfo:
                p_catinfo = MCategory.get_by_uid(catinfo.pid)

        kwd = {
            'pager': '',
            'url': self.request.uri,
            'cookie_str': cookie_str,
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
        MPost.update_misc(postinfo.uid, count=True)
        if self.get_current_user():
            MUsage.add_or_update(self.userinfo.uid, postinfo.uid, postinfo.kind)
        self.set_cookie('user_pass', cookie_str)

        tmpl = self.ext_tmpl_view(postinfo)

        if self.userinfo:
            recent_apps = MUsage.query_recent(self.userinfo.uid, postinfo.kind, 6).naive()[1:]
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
                    tag_info=MPost2Label.get_by_uid(postinfo.uid).naive(),
                    recent_apps=recent_apps,
                    cat_enum=cat_enum1)

    def fetch_additional_posts(self, uid):
        '''
        fetch the rel_recs, and random recs when view the post.
        :param postinfo:
        :return:
        '''
        cats = MPost2Catalog.query_by_entity_uid(uid, kind=self.kind)
        cat_uid_arr = []
        for cat_rec in cats:
            cat_uid = cat_rec.tag_id
            cat_uid_arr.append(cat_uid)
        logger.info('info category: {0}'.format(cat_uid_arr))
        rel_recs = MRelation.get_app_relations(uid, 8, kind=self.kind).naive()

        logger.info('rel_recs count: {0}'.format(rel_recs.count()))
        if len(cat_uid_arr) > 0:
            rand_recs = MPost.query_cat_random(cat_uid_arr[0], limit=4 - rel_recs.count() + 4)
        else:
            rand_recs = MPost.query_random(num=4 - rel_recs.count() + 4, kind=self.kind)
        return rand_recs, rel_recs

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

    def fetch_post_data(self):
        '''
        fetch post accessed data. post_data, and ext_dic.
        :return:
        '''
        post_data = {}
        ext_dic = {}
        for key in self.request.arguments:
            if key.startswith('ext_') or key.startswith('tag_'):
                ext_dic[key] = self.get_argument(key)
            else:
                post_data[key] = self.get_arguments(key)[0]

        post_data['user_name'] = self.userinfo.user_name
        post_data['kind'] = self.kind

        # append external infor.

        if 'tags' in post_data:
            ext_dic['def_tag_arr'] = [x.strip() for x
                                      in post_data['tags'].strip().strip(',').split(',')]
        ext_dic = dict(ext_dic, **self.ext_post_data(postdata=post_data))

        return (post_data, ext_dic)

    @tornado.web.authenticated
    @tornado.web.asynchronous
    # @tornado.gen.coroutine
    def add(self, **kwargs):
        '''
        in infor.
        :param kwargs:
        :return:
        '''
        if 'uid' in kwargs:
            uid = kwargs['uid']
        else:
            uid = self._gen_uid()

        if self.check_post_role()['ADD']:
            pass
        else:
            return False

        post_data, ext_dic = self.fetch_post_data()

        if 'valid' in post_data:
            post_data['valid'] = int(post_data['valid'])
        else:
            post_data['valid'] = 1

        ext_dic['def_uid'] = uid

        MPost.modify_meta(ext_dic['def_uid'],
                          post_data,
                          extinfo=ext_dic)
        kwargs.pop('uid', None)  # delete `uid` if exists in kwargs
        self.update_tag(uid=ext_dic['def_uid'], **kwargs)

        # cele_gen_whoosh.delay()
        tornado.ioloop.IOLoop.instance().add_callback(self.cele_gen_whoosh)
        self.redirect('/{0}/{1}'.format(router_post[self.kind], uid))

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

        post_data, ext_dic = self.fetch_post_data()

        if 'valid' in post_data:
            post_data['valid'] = int(post_data['valid'])
        else:
            post_data['valid'] = postinfo.valid

        ext_dic['def_uid'] = str(uid)

        cnt_old = tornado.escape.xhtml_unescape(postinfo.cnt_md).strip()
        cnt_new = post_data['cnt_md'].strip()
        if cnt_old == cnt_new:
            pass
        else:
            MPostHist.create_post_history(postinfo)

        MPost.modify_meta(uid, post_data, extinfo=ext_dic)

        self.update_tag(uid=uid)

        logger.info('post kind:' + self.kind)
        # cele_gen_whoosh.delay()
        tornado.ioloop.IOLoop.instance().add_callback(self.cele_gen_whoosh)
        self.redirect('/{0}/{1}'.format(router_post[postinfo.kind], uid))

    @tornado.web.authenticated
    def delete(self, *args, **kwargs):
        '''
        delete the post.
        :param args:
        :param kwargs:
        :return:
        '''
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

    @deprecated(details='you should use: /post_j/delete')
    @tornado.web.authenticated
    def j_delete(self, uid):
        '''
        Delete the post, but return the JSON.
        :param uid:
        :return:
        '''

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

    @deprecated(deprecated_in='0.5', removed_in='0.6', details='you should use: /post_j/count_plus')
    def j_count_plus(self, uid):
        '''
        Ajax request, that the view count will plus 1.
        :param uid:
        :return:
        '''
        self.set_header("Content-Type", "application/json")
        output = {
            'status': 1  # if MPost.__update_view_count_by_uid(uid) else 0,
        }
        self.write(json.dumps(output))

    def _chuli_cookie_relation(self, app_id):
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

    def ext_view_kwd(self, postinfo):
        '''
        The additional information. for View.
        :param postinfo:
        :return: directory.
        '''
        return {}

    def ext_tmpl_view(self, rec):
        '''
        Used for self defined templates. for View.
        :param rec:
        :return:
        '''
        return self._get_tmpl_view(rec)

    def ext_post_data(self, **kwargs):
        '''
        The additional information.  for add(), or update().
        :param post_data:
        :return: directory.
        '''
        return {}

    @tornado.web.authenticated
    def _to_edit_kind(self, post_uid):
        '''
        Show the page for changing the category.
        :param post_uid:
        :return:
        '''
        if self.userinfo and self.userinfo.role[1] >= '3':
            pass
        else:
            self.redirect('/')
        postinfo = MPost.get_by_uid(post_uid, )
        json_cnt = json.dumps(postinfo.extinfo, indent=True)
        self.render('man_info/post_kind.html',
                    postinfo=postinfo,
                    sig_dic=router_post,
                    userinfo=self.userinfo,
                    unescape=tornado.escape.xhtml_unescape,
                    json_cnt=json_cnt)

    @tornado.web.authenticated
    def _change_kind(self, post_uid):
        '''
        To modify the category of the post, and kind.
        :param post_uid:
        :return:
        '''
        if self.userinfo and self.userinfo.role[1] >= '3':
            pass
        else:
            return False
        post_data = self.get_post_data()

        logger.info('admin post update: {0}'.format(post_data))

        MPost.update_misc(post_uid, kind=post_data['kcat'])
        self.update_category(post_uid)
        self.redirect('/{0}/{1}'.format(router_post[post_data['kcat']], post_uid))
