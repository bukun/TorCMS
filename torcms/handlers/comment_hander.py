import tornado.web

import config
from config import CMS_CFG, post_cfg
from torcms.core import privilege
from torcms.core.base_handler import BaseHandler
from torcms.model.comment_model import MComment


class CommentHandler(BaseHandler):
    def initialize(self):
        super().initialize()

    def get(self, *args, **kwargs):
        url_str = args[0]
        url_arr = self.parse_url(url_str)
        if url_str == '' or url_str == 'list':
            self.list(url_str)
        elif len(url_arr) == 2:
            self.list(url_arr[0], cur_p=url_arr[1])

    @tornado.web.authenticated
    @privilege.permission(action='assign_role')
    def list(self, list, **kwargs):
        '''
        List the replies.
        '''

        def get_pager_idx():
            '''
            Get the pager index.
            '''
            cur_p = kwargs.get('cur_p')
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
            return current_page_number

        current_page_num = get_pager_idx()
        num_of_cat = MComment.count_of_certain()
        page_num = int(num_of_cat / CMS_CFG['list_num']) + 1

        kwd = {
            'current_page': current_page_num,
            'count': num_of_cat,
        }
        self.render(
            'static_pages/comment/index.html',
            postinfo=MComment.query_pager_by_comment(current_page_num),
            userinfo=self.userinfo,
            cfg=CMS_CFG,
            kwd=kwd,
            router_post=post_cfg,
        )
