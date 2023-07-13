# -*- coding:utf-8 -*-
'''
Handler for role.
'''

import json
import tornado.web
from torcms.core import tools, privilege
from torcms.core.base_handler import BaseHandler
from torcms.model.role_model import MRole
from torcms.model.role2permission_model import MRole2Permission


class RoleHandler(BaseHandler):
    '''
    Handler for role.
    '''

    def initialize(self, **kwargs):
        super().initialize()
        self.kind = 'u'

    def get(self, *args, **kwargs):
        url_str = args[0]
        url_arr = self.parse_url(url_str)

        if url_str == 'list':
            self.recent()
        elif url_arr[0] == 'get':
            self.get_by_id(url_arr[1])
        elif url_arr[0] == 'chainedOptions':
            self.chainedOptions()
        elif url_arr[0] == 'getpid':
            self.getpid()

        else:
            kwd = {
                'info': '页面未找到',
            }
            self.render(
                'misc/html/404.html',
                kwd=kwd,
                userinfo=self.userinfo,
            )

    def post(self, *args, **kwargs):
        url_str = args[0]

        if url_str == '':
            return
        url_arr = self.parse_url(url_str)

        if url_arr[0] == '_edit':
            self.update(url_arr[1])
        elif url_arr[0] == '_delete':
            self.delete_by_id(url_arr[1])
        elif url_arr[0] == '_add':
            self.role_add()
        elif url_arr[0] == 'batch_edit':
            self.batch_edit()
        elif url_arr[0] == 'batch_delete':
            self.batch_delete(url_arr[1])

        else:
            self.redirect('misc/html/404.html')

    def getpid(self):

        dics = [{"label": "无", "value": "0000"}]
        recs = MRole.query_all()

        for rec in recs:
            dic = {"label": rec.name, "value": rec.uid}

            dics.append(dic)
        out_dict = {"ok": True, "status": 0, 'data': dics}

        return json.dump(out_dict, self, ensure_ascii=False)

    def chainedOptions(self):
        '''
        Recent links.
        '''

        post_data = self.request.arguments  # {'page': [b'1'], 'perPage': [b'10']}

        parentId = post_data['parentId'][0].decode('utf-8')
        if parentId == '':
            parentId = '0000'
        dics = []
        recs = MRole.get_by_pid(parentId)
        

        for rec in recs:
            dic = {"label": rec.name, "value": rec.uid}

            dics.append(dic)
        out_dict = {"ok": True, "status": 0, 'data': dics}

        return json.dump(out_dict, self, ensure_ascii=False)

    def recent(self):
        '''
        Recent links.
        '''

        post_data = self.request.arguments  # {'page': [b'1'], 'perPage': [b'10']}
        page = int(post_data['page'][0].decode('utf-8'))
        perPage = int(post_data['perPage'][0].decode('utf-8'))

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
        dics = []
        recs = MRole.query_all_pager(current_page_num, perPage)
        counts = MRole.get_counts_by_pid()

        for rec in recs:
            dic = self.get_recs_dic(rec)

            childrens1 = MRole.get_by_pid(rec.uid)
            chid_dics1 = []
            for children1 in childrens1:
                chid1_rec = self.get_recs_dic(children1)

                childrens2 = MRole.get_by_pid(children1.uid)
                chid_dics2 = []
                for child2 in childrens2:
                    chid2_rec = self.get_recs_dic(child2)

                    chid_dics2.append(chid2_rec)
                if chid_dics2:
                    chid1_rec['children'] = chid_dics2

                chid_dics1.append(chid1_rec)
            if chid_dics1:
                dic['children'] = chid_dics1

            dics.append(dic)
        out_dict = {
            "ok": True,
            "status": 0,
            "msg": "ok",
            "data": {"count": counts, "rows": dics},
        }

        return json.dump(out_dict, self, ensure_ascii=False)

    def get_recs_dic(self, rec):
        rec = {
            "uid": rec.uid,
            "name": rec.name,
            "status": rec.status,
            "pid": rec.pid,
            "time_create": tools.format_time(rec.time_create),
            "time_update": tools.format_time(rec.time_update),
            "permission": self.get_permission(rec.uid),
            "pid_name": self.get_pid_name(rec.pid)
        }
        return rec

    def get_permission(self, uid):
        pers = MRole2Permission.query_permission_by_role(uid)
        per_arr = []
        for per in pers:
            per_arr.append(per['name'])
        return per_arr

    def get_pid_name(self, uid):
        pid_rec = MRole.get_by_uid(uid)
        if pid_rec:
            pid_name = pid_rec.name
        else:
            pid_name = '无'
        return pid_name

    def get_by_id(self, uid):
        rec = MRole.get_by_uid(uid)

        dic = [
            {
                "uid": rec.uid,
                "name": rec.name,
                "status": rec.status,
                "pid": rec.pid,
                "time_create": tools.format_time(rec.time_create),
                "time_update": tools.format_time(rec.time_update),
            }
        ]

        out_dict = {"title": "分组/角色详情", "rolemore_table": dic}

        return json.dump(out_dict, self, ensure_ascii=False)

    @privilege.permission(action='assign_group')
    @tornado.web.authenticated
    def update(self, uid):
        '''
        Update the link.
        '''

        post_data = json.loads(self.request.body)
        per_dics = post_data.get("permission").split(",")
        per_recs = MRole2Permission.query_by_role(uid)

        for rec in per_recs:
            MRole2Permission.remove_relation(uid, rec.permission)

        if MRole.update(uid, post_data):
            if per_dics:
                for per in per_dics:
                    if per:
                        MRole2Permission.add_or_update(uid, per)

                role_recs = MRole.get_by_pid(uid)
                if role_recs:
                    for role_rec in role_recs:

                        per_recs = MRole2Permission.query_by_role(role_rec.uid)

                        for rec1 in per_recs:

                            if str(rec1.permission) in per_dics:
                                print(rec1.permission)
                                continue
                            else:
                                MRole2Permission.remove_relation(role_rec.uid, rec1.permission)

            output = {
                "ok": True,
                "status": 0,
                "msg": "更新分组/角色成功"
            }


        else:
            output = {
                "ok": False,
                "status": 404,
                "msg": "更新分组/角色失败"
            }

        return json.dump(output, self, ensure_ascii=False)

    @privilege.permission(action='assign_group')
    @tornado.web.authenticated
    def batch_edit(self):
        '''
        Update the link.
        '''

        post_data = json.loads(self.request.body)

        ids = post_data.get("ids", "").split(",")
        per_dics = post_data.get("permission", "").split(",")
        for uid in ids:
            recs = MRole2Permission.query_by_role(uid)

            for rec in recs:
                MRole2Permission.remove_relation(uid, rec.permission)

            if MRole.update(uid, post_data):
                if per_dics:
                    for per in per_dics:
                        MRole2Permission.add_or_update(uid, per)

                role_recs = MRole.get_by_pid(uid)
                if role_recs:
                    for role_rec in role_recs:

                        per_recs = MRole2Permission.query_by_role(role_rec.uid)

                        for rec1 in per_recs:

                            if str(rec1.permission) in per_dics:
                                print(rec1.permission)
                                continue
                            else:
                                MRole2Permission.remove_relation(role_rec.uid, rec1.permission)

                output = {
                    "ok": True,
                    "status": 0,
                    "msg": "更新分组/角色成功"
                }

            else:
                output = {
                    "ok": False,
                    "status": 404,
                    "msg": "批量更新分组/角色失败"
                }
        return json.dump(output, self, ensure_ascii=False)

    @privilege.permission(action='assign_group')
    @tornado.web.authenticated
    def role_add(self):
        '''
        user add link.
        '''

        post_data = json.loads(self.request.body)
        per_dics = post_data.get("permission", "").split(",")

        cur_uid = tools.get_uudd(2)
        while MRole.get_by_uid(cur_uid):
            cur_uid = tools.get_uudd(2)
        role_uid = MRole.add_or_update(cur_uid, post_data)
        if role_uid:
            if per_dics:
                for per in per_dics:
                    print(per)
                    MRole2Permission.add_or_update(role_uid, per)
            output = {
                "ok": True,
                "status": 0,
                "msg": "添加/更新分组/角色成功"
            }
        else:
            output = {
                "ok": False,
                "status": 404,
                "msg": "添加/更新分组/角色失败"
            }
        return json.dump(output, self, ensure_ascii=False)

    @privilege.permission(action='assign_group')
    @tornado.web.authenticated
    def delete_by_id(self, del_id):
        '''
        Delete a link by id.
        '''
        del_roles = MRole2Permission.query_by_role(del_id)
        for del_role in del_roles:
            MRole2Permission.remove_relation(del_role.role, del_role.permission)

        if MRole.delete(del_id):
            output = {
                "ok": True,
                "status": 0,
                "msg": "删除分组/角色成功"}
        else:
            output = {
                "ok": False,
                "status": 404,
                "msg": "删除分组/角色失败"}
        return json.dump(output, self, ensure_ascii=False)

    @privilege.permission(action='assign_group')
    @tornado.web.authenticated
    def batch_delete(self, del_id):
        '''
        Delete a link by id.
        '''

        del_uids = del_id.split(",")
        for del_id in del_uids:
            del_roles = MRole2Permission.query_by_role(del_id)
            for del_role in del_roles:
                MRole2Permission.remove_relation(del_role.role, del_role.permission)

            if MRole.delete(del_id):
                output = {
                    "ok": True,
                    "status": 0,
                    "msg": "删除分组/角色成功"}
            else:
                output = {
                    "ok": False,
                    "status": 404,
                    "msg": "删除分组/角色失败"}
        return json.dump(output, self, ensure_ascii=False)
