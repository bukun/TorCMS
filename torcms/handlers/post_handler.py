# -*- coding:utf-8 -*-

'''
The basic HTML Page handler.
'''

import json

import tornado.escape
import tornado.web

from config import cfg
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


class PostHandler(BaseHandler):
    '''
    The basic HTML Page handler.
    '''

    def initialize(self):
        super(PostHandler, self).initialize()
        self.mpost = MPost()
        self.mcat = MCategory()
        self.mpost_hist = MPostHist()
        self.mpost2catalog = MPost2Catalog()
        self.mpost2label = MPost2Label()
        self.mrel = MRelation()
        self.kind = '1'

    def get(self, *args):

        url_str = args[0]
        url_arr = self.parse_url(url_str)

        if url_str == '':
            self.index()
        elif len(url_arr) == 1 and url_str.endswith('.html'):
            # Deprecated
            self.view_or_add(url_str.split('.')[0])
        elif url_arr[0] in ['add_document', '_add']:
            self.to_add()
        elif url_str == 'recent':
            self.recent()
        elif url_str == '_refresh':
            self.refresh()
        elif url_arr[0] in ['modify', 'edit', '_edit']:
            self.to_edit(url_arr[1])
        elif url_arr[0] == 'delete':
            self.delete(url_arr[1])
        elif url_arr[0] == 'j_delete':
            self.j_delete(url_arr[1])
        elif url_arr[0] in ['j_count_plus', 'ajax_count_plus', ]:
            self.j_count_plus(url_arr[1])
        elif len(url_arr) == 1:
            self.view_or_add(url_str)
        else:
            kwd = {
                'info': '404. Page not found!',
            }
            self.render('html/404.html', kwd=kwd,
                        userinfo=self.userinfo, )

    def post(self, *args):
        url_str = args[0]
        logger.info('post url: {0}'.format(url_str))

        url_arr = self.parse_url(url_str)

        if url_arr[0] in ['modify', 'edit', '_edit']:
            self.update(url_arr[1])
        elif url_arr[0] in ['add_document', '_add']:
            self.add()
        elif len(url_arr) == 1:
            if len(url_str) in [4, 5]:
                self.add(uid=url_str)
        else:
            self.redirect('html/404.html')

    def index(self):
        '''
        The default page of POST.
        :return:
        '''
        self.render('post_{0}/index.html'.format(self.kind),
                    userinfo=self.userinfo,
                    kwd={'uid': '',}, )

    def j_count_plus(self, uid):
        '''
        Ajax request, that the view count will plus 1.
        :param uid:
        :return:
        '''
        logger.info('Deprecated, you should use: /post_j/count_plus')
        self.set_header("Content-Type", "application/json")
        output = {
            'status': 1 if self.mpost.update_view_count_by_uid(uid) else 0,
        }
        self.write(json.dumps(output))

    @tornado.web.authenticated
    def extor_data(self, **kwargs):
        '''
        The additional information.
        :param post_data:
        :return: directory.
        '''
        return {}

    def recent(self, with_catalog=True, with_date=True):
        '''
        List posts that recent edited.
        :param with_catalog:
        :param with_date:
        :return:
        '''
        kwd = {
            'pager': '',
            'unescape': tornado.escape.xhtml_unescape,
            'title': 'Recent posts.',
            'with_catalog': with_catalog,
            'with_date': with_date,
        }
        self.render('post_{0}/post_list.html'.format(self.kind),
                    kwd=kwd,
                    view=self.mpost.query_recent(num=20, kind=self.kind),
                    postinfo=self.mpost.query_recent(num=20, kind=self.kind),
                    format_date=tools.format_date,
                    userinfo=self.userinfo,
                    cfg=cfg, )

    @tornado.web.authenticated
    def __could_edit(self, postid):
        post_rec = self.mpost.get_by_uid(postid)
        if post_rec:
            pass
        else:
            return False
        if self.check_post_role(self.userinfo)['EDIT']:
            return True
        elif post_rec.user_name == self.userinfo.user_name:
            return True
        else:
            return False

    def refresh(self):
        '''
        List the post of dated.
        :return:
        '''
        kwd = {
            'pager': '',
            'title': '',
        }
        self.render('post_{0}/post_list.html'.format(self.kind),
                    kwd=kwd,
                    userinfo=self.userinfo,
                    view=self.mpost.query_dated(10),
                    postrecs=self.mpost.query_dated(10),
                    format_date=tools.format_date,
                    unescape=tornado.escape.xhtml_unescape,
                    cfg=cfg, )

    def view_or_add(self, uid):
        '''
        Try to get the post. If not, to add the wiki.
        :param uid:
        :return:
        '''
        postinfo = self.mpost.get_by_uid(uid)
        if self.mpost.get_by_id(uid):
            self.viewinfo(postinfo)
        else:
            self.to_add(uid)

    @tornado.web.authenticated
    def to_add(self, *args):
        # uid = args[0]
        if self.check_post_role(self.userinfo)['ADD']:
            pass
        else:
            return False
        kwd = {
            'pager': '',
            'cats': self.mcat.query_all(),
            'uid': '',
        }
        self.render('post_{0}/post_add.html'.format(self.kind),
                    kwd=kwd,
                    tag_infos=self.mcat.query_all(),
                    userinfo=self.userinfo,
                    cfg=cfg, )

    @tornado.web.authenticated
    def update(self, uid):
        '''
        Update the post according to the uid.
        :param uid:
        :return:
        '''
        if self.__could_edit(uid):
            pass
        else:
            return False

        postinfo = self.mpost.get_by_id(uid)
        if postinfo.kind == self.kind:
            pass
        else:
            return False

        post_data = self.get_post_data()

        post_data['user_name'] = self.get_current_user()
        post_data['kind'] = self.kind
        is_update_time = True if post_data['is_update_time'][0] == '1' else False

        cnt_old = tornado.escape.xhtml_unescape(postinfo.cnt_md).strip()
        cnt_new = post_data['cnt_md'].strip()
        if cnt_old == cnt_new:
            pass
        else:
            self.mpost_hist.insert_data(postinfo)

        logger.info('upadte: {0}'.format(uid))
        logger.info('Update post_data: {0}'.format(post_data))
        self.mpost.update(uid, post_data, update_time=is_update_time)
        self.update_category(uid)
        self.update_tag(uid)
        self.redirect('/{0}/{1}'.format(router_post[postinfo.kind], uid))

    @tornado.web.authenticated
    def update_tag(self, signature):
        '''
        Update the tags when updating.
        :param signature:
        :return:
        '''
        current_tag_infos = self.mpost2label.get_by_id(signature, kind=self.kind)
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
                self.mpost2label.add_record(signature, tag_name, 1)

        for cur_info in current_tag_infos:
            print(cur_info.tag.name)
            if cur_info.tag.name in tags_arr:
                pass
            else:
                self.mpost2label.remove_relation(signature, cur_info.tag)

    @tornado.web.authenticated
    def update_category(self, uid):
        '''
        Update the category of the post.
        :param uid:  The ID of the post. Extra info would get by requests.
        :return:
        '''
        post_data = self.get_post_data()

        current_infos = self.mpost2catalog.query_by_entity_uid(uid)
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
        for idx, val in enumerate(new_tag_arr):
            self.mpost2catalog.add_record(uid, val, idx)

        # Delete the old category if not in post requests.
        for cur_info in current_infos:
            if str(cur_info.tag.uid).strip() not in new_tag_arr:
                self.mpost2catalog.remove_relation(uid, cur_info.tag)

    @tornado.web.authenticated
    def to_edit(self, uid):
        '''
        Show the HTML page for editing the post.
        :param uid:
        :return:
        '''
        if self.__could_edit(uid):
            pass
        else:
            return False

        kwd = {
            'pager': '',
            'cats': self.mcat.query_all(),

        }
        self.render('post_{0}/post_edit.html'.format(self.kind),
                    kwd=kwd,
                    unescape=tornado.escape.xhtml_unescape,
                    tag_infos=self.mcat.query_all(kind=self.kind),
                    app2label_info=self.mpost2label.get_by_id(uid),
                    app2tag_info=self.mpost2catalog.query_by_entity_uid(uid, self.kind),
                    dbrec=self.mpost.get_by_id(uid),
                    userinfo=self.userinfo,
                    cfg=cfg, )

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

        if last_post_id and self.mpost.get_by_id(last_post_id):
            self.add_relation(last_post_id, post_id)

    def viewinfo(self, postinfo):
        post_id = postinfo.uid
        self.__gen_last_current_relation(post_id)
        cats = self.mpost2catalog.query_by_entity_uid(post_id)
        tag_info = self.mpost2label.get_by_id(post_id)
        if postinfo.kind == self.kind:
            pass
        else:
            self.redirect('/{0}/{1}'.format(router_post[postinfo.kind], post_id), permanent=True)

        if not postinfo:
            kwd = {
                'info': '您要查看的页面不存在。',
            }
            self.render('html/404.html',
                        kwd=kwd,
                        userinfo=self.userinfo)
            return False

        if cats.count() == 0:
            cat_id = ''
        else:
            cat_id = cats.get().tag
        kwd = {
            'pager': '',
            'editable': self.editable(),
            'cat_id': cat_id
        }

        rel_recs = self.mrel.get_app_relations(postinfo.uid, 4)
        rand_recs = self.mpost.query_random(4 - rel_recs.count() + 2)

        self.render('post_{0}/post_view.html'.format(self.kind),
                    view=postinfo,
                    postinfo=postinfo,
                    unescape=tornado.escape.xhtml_unescape,
                    kwd=kwd,
                    userinfo=self.userinfo,
                    tag_info=tag_info,
                    relations=rel_recs,
                    rand_recs=rand_recs,
                    replys=[],
                    cfg=cfg, )

    def add_relation(self, f_uid, t_uid):
        if self.mpost.get_by_id(t_uid) is False:
            return False
        if f_uid == t_uid:  # relate to itself.
            return False
        # 双向关联，但权重不一样.
        self.mrel.add_relation(f_uid, t_uid, 2)
        self.mrel.add_relation(t_uid, f_uid, 1)
        return True

    @tornado.web.authenticated
    def add(self, **kwargs):

        if 'uid' in kwargs:
            uid = kwargs['uid']
        else:
            uid = self.__gen_uid()
        if self.check_post_role(self.userinfo)['ADD']:
            pass
        else:
            return False
        post_data = self.get_post_data()
        if 'title' in post_data:
            pass
        else:
            self.set_status(400)
            return False

        post_data['user_name'] = self.userinfo.user_name
        post_data['kind'] = self.kind
        cur_post_rec = self.mpost.get_by_id(uid)
        if cur_post_rec:
            pass
        else:
            if self.mpost.insert_data(uid, post_data):
                self.update_tag(uid)
                self.update_category(uid)
        self.redirect('/{0}/{1}'.format(router_post[self.kind], uid))

    def __gen_uid(self):
        '''
        Generate the ID for post.
        :return: the new ID.
        '''
        new_uid = tools.get_uu5d()
        while self.mpost.get_by_id(new_uid):
            new_uid = tools.get_uu5d()
        return new_uid

    @tornado.web.authenticated
    def delete(self, *args, **kwargs):
        '''
        Delete the post.
        :param uid: The ID to be deleted.
        :return:
        '''
        uid = args[0]
        if self.check_post_role(self.userinfo)['DELETE']:
            pass
        else:
            return False
        if self.mpost.delete(uid):
            self.redirect('/{0}/recent'.format(router_post[self.kind]))
        else:
            return False

    @tornado.web.authenticated
    def j_delete(self, uid):
        '''
        Delete the post, but return the JSON.
        :param uid:
        :return:
        '''
        logger.info('Deprecated, you should use: /post_j/delete')

        if self.check_post_role(self.userinfo)['DELETE']:
            pass
        else:
            return False
        is_deleted = self.mpost.delete(uid)

        if is_deleted:
            output = {
                'del_info ': 1,
            }
        else:
            output = {
                'del_info ': 0,
            }
        return json.dump(output, self)
