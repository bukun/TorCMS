import config
from torcms.core.base_handler import BaseHandler
from torcms.model.comment_model import MComment
from config import CMS_CFG, router_post


class CommentHandler(BaseHandler):
    def initialize(self):
        super(CommentHandler, self).initialize()

    def get(self, *args, **kwargs):
        url_str = args[0]
        url_arr = self.parse_url(url_str)
        if url_str == '' or url_str == 'list':
            self.list(url_str)
        elif len(url_arr) == 2:
            self.list(url_arr[0], cur_p=url_arr[1])

    def list(self, list, **kwargs):
        '''
        List the replies.
        '''

        def get_pager_idx():
            '''
            Get the pager index.
            '''
            cur_p = kwargs.get('cur_p')
            the_num = int(cur_p) if cur_p else 1
            the_num = 1 if the_num < 1 else the_num
            return the_num

        current_page_num = get_pager_idx()
        num_of_cat = MComment.count_of_certain()
        page_num = int(num_of_cat / CMS_CFG['list_num']) + 1

        kwd = {
            'current_page': current_page_num,
            'count': num_of_cat,

        }
        self.render('static_pages/comment/index.html',
                    postinfo=MComment.query_pager_by_comment(current_page_num),
                    userinfo=self.userinfo,
                    cfg=CMS_CFG,
                    kwd=kwd,
                    router_post=router_post)
