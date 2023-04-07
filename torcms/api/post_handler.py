'''
Handler of Posts via Ajax.
'''
import json

import tornado.escape
import tornado.web
from config import post_cfg
from torcms.core import privilege, tools
from torcms.handlers.post_handler import PostHandler
from torcms.model.post_model import MPost
from torcms.model.category_model import MCategory


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

        if url_arr[0] == 'list':
            self.list(url_arr[1])

    def post(self, *args, **kwargs):
        url_str = args[0]

        if url_str == '':
            return
        url_arr = self.parse_url(url_str)

        if url_arr[0] == '_edit':
            self.update(url_arr[1])
        elif url_arr[0] == '_delete':
            self.delete(url_arr[1])

        # elif url_arr[0] == 'batch_edit':
        #     self.batch_edit()
        elif url_arr[0] == 'batch_delete':
            self.batch_delete(url_arr[1])

        else:
            self.redirect('misc/html/404.html')

    def list(self, kind):

        post_data = self.request.arguments  # {'page': [b'1'], 'perPage': [b'10']}
        page = int(str(post_data['page'][0])[2:-1])
        perPage = int(str(post_data['perPage'][0])[2:-1])

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

        current_page_num = get_pager_idx()

        recs = MPost.query_pager_by_slug(kind, current_page_num, perPage)
        # 分类筛选用以下方法
        # recs = MPost.query_list_pager(kind, current_page_num, perPage)
        counts = MPost.total_number(kind)
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
                    "router": post_cfg[kind]['router']
                }
            )

        output = {
            "ok": True,
            "status": 0,
            "msg": "ok",
            "data": {"count": counts, "rows": rec_arr}
        }
        return json.dump(output, self, ensure_ascii=False)

    @tornado.web.authenticated
    @privilege.permission(action='can_delete')
    def delete(self, del_id):
        '''
        Delete the post, but return the JSON.
        '''

        current_infor = MPost.get_by_uid(del_id)
        is_deleted = MPost.delete(del_id)
        MCategory.update_count(current_infor.extinfo['def_cat_uid'])
        if is_deleted:
            output = {
                "ok": True,
                "status": 0,
                "msg": "删除成功"
            }
        else:
            output = {
                "ok": True,
                "status": 0,
                "msg": "删除失败"
            }
        return json.dump(output, self, ensure_ascii=False)

    @privilege.permission(action='can_delete')
    @tornado.web.authenticated
    def batch_delete(self, del_id):
        '''
        Delete a link by id.
        '''

        del_uids = del_id.split(",")
        for del_id in del_uids:
            current_infor = MPost.get_by_uid(del_id)
            is_deleted = MPost.delete(del_id)
            MCategory.update_count(current_infor.extinfo['def_cat_uid'])
            if is_deleted:
                output = {
                    "ok": True,
                    "status": 0,
                    "msg": "删除成功"
                }
            else:
                output = {
                    "ok": True,
                    "status": 0,
                    "msg": "删除失败"
                }

        return json.dump(output, self, ensure_ascii=False)
