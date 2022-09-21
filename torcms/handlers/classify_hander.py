from config import CMS_CFG, router_post
from torcms.core.base_handler import BaseHandler
from torcms.model.classify_model import MClassify


class ClassifyHandler(BaseHandler):
    def initialize(self):
        super().initialize()

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
