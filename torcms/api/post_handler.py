'''
Handler of Posts via Ajax.
'''
import json

import tornado.escape
import tornado.web

from torcms.core import privilege, tools
from torcms.handlers.post_handler import PostHandler
from torcms.model.post_model import MPost


class ApiPostHandler(PostHandler):
    '''
    Handler of Posts via Ajax.
    '''

    def initialize(self, **kwargs):
        super().initialize()
        self.kind = '1'

    def get(self, *args, **kwargs):
        url_str = args[0]
        url_arr = self.parse_url(args[0])
        print("-" * 50)
        print(url_str)
        print(url_arr)
        if url_str == 'list':
            self.list()


    def list(self):

        post_data = self.request.arguments  # {'page': [b'1'], 'perPage': [b'10']}
        page = int(str(post_data['page'][0])[2:-1])
        perPage = int(str(post_data['perPage'][0])[2:-1])

        # kind = post_data.get('kind', 1)
        # with_catalog = post_data.get('with_catalog', True)
        # with_date = post_data.get('with_date', True)

        def get_pager_idx():
            '''
            Get the pager index.
            '''

            current_page_number = 1
            if page == '':
                current_page_number = 1
            else:
                try:
                    current_page_number = int(page)
                except TypeError:
                    current_page_number = 1
                except Exception as err:
                    print(err.args)
                    print(str(err))
                    print(repr(err))

            current_page_number = 1 if current_page_number < 1 else current_page_number
            return current_page_number

        num = get_pager_idx()

        recs = MPost.query_recent(num=num, kind='1')
        counts = recs.count()
        rec_arr = []

        for rec in recs:
            rec_arr.append(
                {
                    "uid": rec.uid,
                    "title": rec.title,
                    "cnt_md": rec.cnt_md,
                    "cnt_html": tornado.escape.xhtml_unescape(rec.cnt_html),
                    "user_name": rec.user_name,
                    "keywords": rec.keywords,
                    "logo": rec.logo,
                    "kind": rec.kind,
                    "state": rec.state,
                    "time_create": tools.format_time(rec.time_create),
                    "time_update": tools.format_time(rec.time_update),
                    "view_count": rec.view_count,
                    "rating": rec.rating,
                    "valid": rec.valid,
                    "order": rec.order,
                    "extinfo": rec.extinfo,
                }
            )

        output = {
            "ok": True,
            "status": 0,
            "msg": "ok",
            "data": {"count": counts, "rows": rec_arr}
        }
        return json.dump(output, self, ensure_ascii=False)
