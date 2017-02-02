# -*- coding:utf-8 -*-

import json

import tornado.web

from torcms.handlers.post_handler import PostHandler


class PostAjaxHandler(PostHandler):
    def initialize(self):
        super(PostAjaxHandler, self).initialize()

    def get(self, *args, **kwargs):

        url_arr = self.parse_url(args[0])
        if url_arr[0] == 'delete':
            self.delete(url_arr[1])
        elif url_arr[0] in ['count_plus']:
            self.count_plus(url_arr[1])

    @tornado.web.authenticated
    def delete(self, *args, **kwargs):
        '''
        Delete the post via Ajax request.
        :param args:
        :param kwargs:
        :return:
        '''
        uid = args[0]
        if self.check_post_role()['DELETE']:
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

    def count_plus(self, uid):
        '''
        Ajax request, that the view count will plus 1.
        :param uid:
        :return:
        '''
        self.set_header("Content-Type", "application/json")
        output = {
            'status': 1 if self.mpost.update_view_count_by_uid(uid) else 0,
        }
        # return json.dump(output, self)
        self.write(json.dumps(output))
