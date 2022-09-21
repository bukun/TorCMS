'''
listing the posts, simply.
'''

from config import CMS_CFG
from torcms.core import tools
from torcms.core.base_handler import BaseHandler
from torcms.model.post2catalog_model import MPost2Catalog
from torcms.model.post_model import MPost


class PostListHandler(BaseHandler):
    '''
    listing the posts, simply.
    '''

    def initialize(self, **kwargs):
        super().initialize()

    def get(self, *args, **kwargs):

        url_str = args[0]

        dict_get = {
            '_recent': self.recent,
            'recent': self.recent,
            '_refresh': self.refresh,
            'errcat': self.errcat,
        }

        def fun404():
            kwd = {
                'info': '404. Page not found!',
            }
            self.render(
                'misc/html/404.html',
                kwd=kwd,
                userinfo=self.userinfo,
            )

        dict_get.get(url_str, fun404)()

    def recent(self, with_catalog=True, with_date=True):
        '''
        List posts that recent edited.
        '''
        kwd = {
            'pager': '',
            'title': 'Recent posts.',
            'with_catalog': with_catalog,
            'with_date': with_date,
        }
        self.render(
            'list/post_list.html',
            kwd=kwd,
            view=MPost.query_recent(num=20),
            postrecs=MPost.query_recent(num=2),
            format_date=tools.format_date,
            userinfo=self.userinfo,
            cfg=CMS_CFG,
        )

    def errcat(self):
        '''
        List the posts to be modified.
        '''
        post_recs = MPost.query_random(limit=1000)
        outrecs = []
        errrecs = []
        idx = 0
        for postinfo in post_recs:
            if idx > 16:
                break
            cat = MPost2Catalog.get_first_category(postinfo.uid)
            if cat:
                if 'def_cat_uid' in postinfo.extinfo:
                    if postinfo.extinfo['def_cat_uid'] == cat.tag_id:
                        pass
                    else:
                        errrecs.append(postinfo)
                        idx += 1
                else:
                    errrecs.append(postinfo)
                    idx += 1
            else:
                outrecs.append(postinfo)
                idx += 1
        self.render('list/errcat.html',
                    kwd={},
                    norecs=outrecs,
                    errrecs=errrecs,
                    userinfo=self.userinfo)

    def refresh(self):
        '''
        List the post of dated.
        '''
        kwd = {
            'pager': '',
            'title': '',
        }
        self.render('list/post_list.html',
                    kwd=kwd,
                    userinfo=self.userinfo,
                    view=MPost.query_dated(10),
                    postrecs=MPost.query_dated(10),
                    format_date=tools.format_date,
                    cfg=CMS_CFG)
