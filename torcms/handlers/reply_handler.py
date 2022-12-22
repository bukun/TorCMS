# -*- coding:utf-8 -*-
'''
Handler for reply.
'''

import json
import datetime
from config import CMS_CFG
from torcms.core.base_handler import BaseHandler
from torcms.core.tools import logger
from torcms.model.reply2user_model import MReply2User
from torcms.model.reply_model import MReply
from torcms.model.replyid_model import MReplyid


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)


class ReplyHandler(BaseHandler):
    '''
    Handler for reply.
    '''

    def initialize(self):
        super().initialize()

    def get(self, *args, **kwargs):
        url_str = args[0]
        url_arr = self.parse_url(url_str)
        if url_arr[0] == 'get':
            self.get_by_id(url_arr[1])
        if url_arr[0] == 'more':
            self.more_by_id(url_arr[1])
        if url_arr[0] == 'list':
            self.list(url_arr[1])
        elif url_arr[0] == 'get_comment':
            self.get_by_id_comment(url_arr[1])
        elif url_arr[0] == 'delete':
            self.delete(url_arr[1])
        elif url_arr[0] == 'delete_com':
            self.delete_com(url_arr[1])
        elif url_arr[0] == 'zan':

            self.zan(url_arr[1])
        elif url_arr[0] == '_add':
            self._add()

    def post(self, *args, **kwargs):
        url_str = args[0]
        url_arr = self.parse_url(url_str)

        if url_arr[0] == 'add':
            # post reply
            self.add(url_arr[1])
        elif url_arr[0] == '_add':
            # question
            self.json_add()
        elif url_arr[0] == 'add_reply':
            self.add_reply(url_arr[1], url_arr[2])
        elif url_arr[0] == 'modify':
            self.modify(url_arr[1], url_arr[2])

    def _add(self):
        '''
        提问
        '''

        kwd = {

        }
        if self.is_p:
            self.render('admin/reply_ajax/reply_add.html',
                        kwd=kwd,
                        userinfo=self.userinfo)
        else:
            self.render('reply/reply_add.html',
                        kwd=kwd,
                        userinfo=self.userinfo)

    def list(self, cur_p=''):
        '''
        List the replies.
        '''
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

        postdata = self.get_request_arguments()
        ext_field = postdata.get('ext_field', '')
        isjson = postdata.get('isjson', False)

        kwd = {
            'pager': '',
            'current_page': current_page_number,
            'title': '单页列表',
            'num_of_reply': MReply.total_number(),
            'ext_field': ext_field
        }
        infos = MReply.query_pager(current_page_num=current_page_number, ext_field=ext_field)

        if isjson:
            list = []
            for rec in infos:
                dic = {
                    'uid': rec.uid,
                    'cnt_md': rec.cnt_md,
                    'date': rec.date,
                    'timestamp': rec.timestamp,
                    'category': rec.category,
                    'user_name': rec.user_name,
                    'vote': rec.vote,
                    'curp': current_page_number,
                    'extinfo': rec.extinfo
                }

                list.append(dic)

            out_dict = {
                'results': list
            }

            return json.dump(out_dict, self, cls=DateEncoder, ensure_ascii=False)
        elif self.is_p:
            self.render(
                'admin/reply_ajax/reply_list.html',
                kwd=kwd,
                view_all=MReply.query_all(),
                infos=infos,
                userinfo=self.userinfo)
        else:
            self.render(
                'reply/reply_list.html',
                kwd=kwd,
                view_all=MReply.query_all(),
                infos=infos,
                userinfo=self.userinfo)

    def get_by_id(self, reply_id):
        '''
        Get the reply by id.
        '''
        reply = MReply.get_by_uid(reply_id)
        logger.info('get_reply: {0}'.format(reply_id))
        postdata = self.get_request_arguments()
        isjson = postdata.get('isjson', False)
        if isjson:
            list = []

            dic = {
                'uid': reply.uid,
                'cnt_md': reply.cnt_md,
                'username': reply.user_name,
                'date': reply.date,
                'timestamp': reply.timestamp,
                'category': reply.category,
                'user_name': reply.user_name,
                'vote': reply.vote,
                'extinfo': reply.extinfo
            }

            list.append(dic)

            out_dict = {
                'results': list
            }

            return json.dump(out_dict, self, cls=DateEncoder, ensure_ascii=False)

        elif self.is_p:
            self.render('admin/reply_ajax/show_reply.html',
                        reply=reply,
                        username=reply.user_name,
                        date=reply.date,
                        vote=reply.vote,
                        uid=reply.uid,
                        userinfo=self.userinfo,
                        kwd={})
        else:
            self.render('misc/reply/show_reply.html',
                        reply=reply,
                        username=reply.user_name,
                        date=reply.date,
                        vote=reply.vote,
                        uid=reply.uid,
                        userinfo=self.userinfo,
                        kwd={})

    def more_by_id(self, reply_id):
        '''
        Get the reply by id.
        '''
        reply = MReply.get_by_uid(reply_id)

        self.render('reply/show_reply.html',
                    reply=reply,
                    username=reply.user_name,
                    date=reply.date,
                    vote=reply.vote,
                    uid=reply.uid,
                    userinfo=self.userinfo,
                    kwd={})

    def get_by_id_comment(self, reply_id):
        '''
        Get the reply by id.
        '''
        reply = MReply.get_by_uid(reply_id)
        logger.info('get_reply: {0}'.format(reply_id))
        postdata = self.get_request_arguments()
        isjson = postdata.get('isjson', False)
        if isjson:
            list = []

            dic = {
                'uid': reply.uid,
                'cnt_md': reply.cnt_md,
                'username': reply.user_name,
                'date': reply.date,
                'timestamp': reply.timestamp,
                'category': reply.category,
                'user_name': reply.user_name,
                'vote': reply.vote,
                'extinfo': reply.extinfo
            }

            list.append(dic)

            out_dict = {
                'results': list
            }

            return json.dump(out_dict, self, cls=DateEncoder, ensure_ascii=False)

        else:
            self.render('misc/reply/show_comment.html',
                        reply=reply,
                        username=reply.user_name,
                        date=reply.date,
                        vote=reply.vote,
                        uid=reply.uid,
                        userinfo=self.userinfo,
                        kwd={})

    def add(self, post_id):
        '''
        Adding reply to a post.
        '''
        post_data = self.get_request_arguments()

        post_data['user_name'] = self.userinfo.user_name
        post_data['user_id'] = self.userinfo.uid
        post_data['post_id'] = post_id
        post_data['category'] = '0'
        replyid = MReply.create_reply(post_data)
        if replyid:
            out_dic = {
                'pinglun': post_data['cnt_reply'],
                'uid': replyid,
                'user_name': post_data['user_name'],
                'category': post_data['category']
            }
            logger.info('add reply result dic: {0}'.format(out_dic))
            return json.dump(out_dic, self, ensure_ascii=False)

    def json_add(self):
        '''
        Adding reply to a post.
        '''
        post_data, ext_data = self.fetch_post_data()

        post_data['user_name'] = self.userinfo.user_name
        post_data['user_id'] = self.userinfo.uid
        post_data['post_id'] = '00000'
        post_data['category'] = '0'
        replyid = MReply.create_reply(post_data, extinfo=ext_data)
        if replyid:
            out_dic = {
                'uid': replyid,
                'pinglun': post_data['cnt_reply'],
                'user_name': post_data['user_name'],
                'category': post_data['category'],
                'ext_field': ext_data.get('ext_field'),
                'thumbnail': ext_data.get('ext_logo'),
                'video': ext_data.get('ext_file')
            }
            logger.info('add reply result dic: {0}'.format(out_dic))
            return json.dump(out_dic, self, ensure_ascii=False)

            # @tornado.web.authenticated

    def zan(self, id_reply):
        '''
        先在外部表中更新，然后更新内部表字段的值。
        有冗余，但是查看的时候避免了联合查询
        '''

        logger.info('zan: {0}'.format(id_reply))

        MReply2User.create_reply(self.userinfo.uid, id_reply)
        cur_count = MReply2User.get_voter_count(id_reply)

        if cur_count:
            MReply.update_vote(id_reply, cur_count)
            output = {'text_zan': cur_count}
        else:
            output = {'text_zan': 0}
        logger.info('zan dic: {0}'.format(cur_count))

        return json.dump(output, self, ensure_ascii=False)

    def delete(self, del_id):
        '''
        Delete the id
        '''
        if MReply2User.delete(del_id):
            output = {'del_zan': 1}
        else:
            output = {'del_zan': 0}
        return json.dump(output, self)

    def delete_com(self, del_id):
        '''
        Delete the reply id
        '''

        if MReply.delete_by_uid(del_id):
            output = {'del_reply': 1}
        else:
            output = {'del_reply': 0}
        return json.dump(output, self)

    def add_reply(self, post_id, reply_id):
        '''
        Adding reply
        '''
        post_data, ext_data = self.fetch_post_data()

        post_data['user_name'] = self.userinfo.user_name
        post_data['user_id'] = self.userinfo.uid
        post_data['post_id'] = post_id
        post_data['category'] = '1'
        # 表里添加回复内容返回存储id
        replyid = MReply.create_reply(post_data, extinfo=ext_data)
        # 在关联表里存储评论id与回复id
        MReplyid.create_replyid(reply_id, replyid)
        if replyid:
            out_dic = {
                'pinglun': post_data['cnt_reply'],
                'uid': replyid,
                'user_name': post_data['user_name'],
                'category': post_data['category']
            }
            logger.info('add reply result dic: {0}'.format(out_dic))
            return json.dump(out_dic, self, ensure_ascii=False)

    def modify(self, pid, cat):
        '''
        Adding comment to a post.
        '''
        post_data = self.get_request_arguments()
        post_data['user_name'] = self.userinfo.user_name
        post_data['user_id'] = self.userinfo.uid
        post_data['category'] = cat
        reply = MReply.modify_by_uid(pid, post_data)

        if reply:
            out_dic = {
                'pinglun': post_data['cnt_reply'],
                'uid': reply,
                'user_name': post_data['user_name'],
                'category': post_data['category']
            }
            logger.info('Modify reply result dic: {0}'.format(out_dic))
            return json.dump(out_dic, self, ensure_ascii=False)


class ReplyAjaxHandler(ReplyHandler):
    '''
    Partially render for user handler.
    '''

    def initialize(self, **kwargs):
        super().initialize()
        self.is_p = True
