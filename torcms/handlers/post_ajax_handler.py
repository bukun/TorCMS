# -*- coding:utf-8 -*-



import json
import tornado.web
import tornado.escape
from torcms.handlers.post_handler import PostHandler
from torcms.model.post_model import MPost


class PostAjaxHandler(PostHandler):
    def initialize(self):
        super(PostAjaxHandler, self).initialize()

    def get(self, *args):
        url_str = args[0]
        url_arr = self.parse_url(args[0])
        if url_arr[0] == 'delete':
            self.delete(url_arr[1])
        elif url_arr[0] in ['count_plus']:
            self.count_plus(url_arr[1])
        elif len(url_arr) == 1 and len(url_str) in [4, 5]:
            self.view_or_add(url_str)

    @tornado.web.authenticated
    def delete(self, *args):
        '''
        Delete the post via Ajax request.
        :param args:
        :return:
        '''
        uid = args[0]
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

    def viewinfo(self, postinfo):
        out_json = {
            'uid': postinfo.uid,
            'time_update': postinfo.time_update,
            'title': postinfo.title,
            'cnt_html': tornado.escape.xhtml_unescape(postinfo.cnt_html),

        }
        self.write(json.dumps(out_json))

    def count_plus(self, uid):
        '''
        Ajax request, that the view count will plus 1.
        :param uid:
        :return:
        '''
        self.set_header("Content-Type", "application/json")
        output = {
            'status': 1  # if MPost.__update_view_count_by_uid(uid) else 0,
        }
        # return json.dump(output, self)
        self.write(json.dumps(output))
