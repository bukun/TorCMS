from torcms.core.base_handler import BaseHandler
from torcms.model.classify_model import MClassify
from config import CMS_CFG, router_post


class ClassifyHandler(BaseHandler):
    def initialize(self):
        super(ClassifyHandler, self).initialize()

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

        kwd = {
            'current_page': current_page_num,

        }
        arr_num = []

        postinfo = MClassify.query_pager_by_classify_all()
        for i in postinfo:
            postnum = MClassify.count_of_classify(i.uid)
            arr_num.append(postnum)

        self.render('static_pages/classify/index.html',
                    postinfo=postinfo,
                    postcount=MClassify.count_of_certain(),
                    userinfo=self.userinfo,

                    cfg=CMS_CFG,
                    kwd=kwd,
                    arr_num=arr_num,
                    router_post=router_post)
