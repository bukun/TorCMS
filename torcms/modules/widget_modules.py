# -*- coding:utf-8 -*-
'''
Define the widget modules for TorCMS.
'''
import tornado.escape
import tornado.web

import config
from torcms.model.category_model import MCategory
from torcms.model.rating_model import MRating
from torcms.model.reply_model import MReply
from torcms.model.replyid_model import MReplyid
from torcms.model.user_model import MUser
from torcms.model.post_model import MPost
from torcms.model.process_model import MState, MTransition, MRequest, MAction, MRequestAction, \
    MTransitionAction,MProcess
from torcms.model.staff2role_model import MStaff2Role

class BaiduShare(tornado.web.UIModule):
    '''
    widget for baidu share.
    '''

    def render(self, *args, **kwargs):
        en = kwargs.get('en', False)
        return self.render_string('modules/widget/baidu_share.html', en=en)


class ReplyPanel(tornado.web.UIModule):
    '''
    the reply panel.
    '''

    def render(self, *args, **kwargs):
        uid = args[0]
        userinfo = args[1]
        en = kwargs.get('en', False)
        topic = kwargs.get('topic', False)

        return self.render_string(
            'modules/widget/reply_panel.html',
            uid=uid,
            replys=MReply.query_by_post(uid),
            userinfo=userinfo,
            linkify=tornado.escape.linkify,
            en=en,
            topic=topic,
        )


class ReplyPanelIndex(tornado.web.UIModule):
    '''
    the reply panel.
    '''

    def render(self, *args, **kwargs):
        uid = args[0]
        userinfo = args[1]
        en = kwargs.get('en', False)

        return self.render_string(
            'modules/widget/reply_panel_index.html',
            uid=uid,
            replys=MReply.query_by_post(uid, reply_count=1),
            userinfo=userinfo,
            linkify=tornado.escape.linkify,
            en=en,
        )


class UserinfoWidget(tornado.web.UIModule, tornado.web.RequestHandler):
    '''
    userinfo widget.
    '''

    def render(self, *args, **kwargs):
        # is_logged = kwargs.get('userinfo', False)
        is_logged = True if ('userinfo' in kwargs and kwargs['userinfo']) else False
        return self.render_string(
            'modules/widget/loginfo.html',
            userinfo=kwargs['userinfo'],
            is_logged=is_logged,
        )


class WidgetEditor(tornado.web.UIModule):
    '''
    editor widget.
    '''

    def render(self, *args, **kwargs):
        router = args[0]
        uid = args[1]
        userinfo = args[2]
        review = kwargs.get('review', True)
        delete = kwargs.get('delete', False)
        nullify = kwargs.get('nullify', False)
        reclass = kwargs.get('reclass', True)
        url = kwargs.get('url', '')
        catid = kwargs.get('catid', '')

        kwd = {
            'router': router,
            'uid': uid,
            'catid': catid,
            'review': review,
            'delete': delete,
            'nullify': nullify,
            'reclass': reclass,
            'url': url,
        }
        return self.render_string(
            'modules/widget/widget_editor.html', kwd=kwd, userinfo=userinfo
        )


class WidgetSearch(tornado.web.UIModule):
    '''
    search widget. Simple searching. searching for all.
    '''

    def render(self, *args, **kwargs):
        # tag_enum = MCategory.query_pcat()
        return self.render_string('modules/widget/widget_search.html')


class StarRating(tornado.web.UIModule):
    '''
    For rating of posts.
    '''

    def render(self, *args, **kwargs):
        postinfo = args[0]
        userinfo = args[1]
        rating = False
        if userinfo:
            rating = MRating.get_rating(postinfo.uid, userinfo.uid)
        if rating:
            pass
        else:
            rating = postinfo.rating
        return self.render_string(
            'modules/widget/star_rating.html',
            postinfo=postinfo,
            userinfo=userinfo,
            rating=rating,
        )


class UseF2E(tornado.web.UIModule):
    '''
    using f2e lib.
    '''

    def render(self, *args, **kwargs):
        f2ename = args[0]
        return self.render_string('modules/usef2e/{0}.html'.format(f2ename))


class UploadPicture(tornado.web.UIModule):
    '''
    Upload picture
    '''

    def render(self, *args, **kwargs):
        return self.render_string('modules/widget/upload_entity_pic.html')


class UploadFile(tornado.web.UIModule):
    '''
    Upload file
    '''

    def render(self, *args, **kwargs):
        return self.render_string('modules/widget/upload_entity_file.html')


class Navigation_menu(tornado.web.UIModule):
    '''
    Web site secondary navigation
    '''

    def render(self, *args, **kwargs):
        kind = args[0]

        title = kwargs.get('title', '')
        filter_view = kwargs.get('filter_view', False)
        slug = kwargs.get('slug', False)
        curinfo = MCategory.query_kind_cat(kind)

        kwd = {
            'title': title,
            'router': config.post_cfg[kind]['router'],
            'kind': kind,
            'filter_view': filter_view,
            'slug': slug,
        }

        return self.render_string(
            'modules/widget/nav_menu.html', pcatinfo=curinfo, kwd=kwd
        )


class CommentList(tornado.web.UIModule):
    '''
    reply list
    '''

    def render(self, *args, **kwargs):
        replyid = kwargs.get('replyid', '')
        userinfo = kwargs.get('userinfo', '')
        en = kwargs.get('en', False)
        res = MReplyid.get_by_rid(replyid)
        datas = []
        for x in res:
            rec = MReply.get_by_uid(x.reply1)
            if rec in datas:
                pass
            else:
                datas.append(rec)
        return self.render_string(
            'modules/widget/comment_list.html', userinfo=userinfo, recs=datas, en=en
        )


class Replycnt(tornado.web.UIModule):
    def render(self, *args, **kwargs):
        replyid = kwargs.get('replyid', '')
        res = MReply.get_by_uid(replyid)
        reply_cnt = res.cnt_md
        return reply_cnt


class Replycount(tornado.web.UIModule):
    def render(self, *args, **kwargs):
        commentid = args[0]
        res = MReplyid.get_by_rid(commentid)
        reply_count = res.count()
        return reply_count


class ReplyRecentcnt(tornado.web.UIModule):
    def render(self, *args, **kwargs):
        commentid = args[0]
        res = MReplyid.get_by_rid(commentid, rec_num=1)
        for x in res:
            rec = MReply.get_by_uid(x.reply1)

            return rec.cnt_md


class Userprofile(tornado.web.UIModule):
    '''
    the reply panel.
    '''

    def render(self, *args, **kwargs):
        user_id = args[0]
        user_name = kwargs.get('user_name', '')
        if user_name:
            rec = MUser.get_by_name(user_id)
        else:
            rec = MUser.get_by_uid(user_id)
        return self.render_string('modules/widget/user_profile.html', rec=rec)


# class State(tornado.web.UIModule):
#     def render(self, *args, **kwargs):
#         postinfo = kwargs.get('postinfo', '')
#         userinfo = kwargs.get('userinfo', '')
#         kind = kwargs.get('kind', '9')
#         post_authority = config.post_cfg[kind]['checker']
#
#         kwd = {
#             'router': config.post_cfg[kind]['router'],
#             'kind': kind,
#             'post_authority': post_authority,
#         }
#         return self.render_string(
#             'modules/post/state.html', postinfo=postinfo, userinfo=userinfo, kwd=kwd
#         )
#


#######################################################################
#         for act in act_recs:
#             act_dic = {"act_name": act['name'], "act_uid": act['uid'], "request_id": istrues.request}
#             act_arr.append(act_dic)
# # 查询该请求中该转换的所有动作是否都为True
# istrues = MRequestAction.query_by_request(request_rec.uid).get()
#
# if istrues.is_complete:
#
#     # 转到下一状态
#     trans = MTransition.get_by_uid(istrues.transition).get()
#     state = MState.get_by_uid(trans.next_state).get()
#
#     print(trans.uid)
#
#     if state.state_type.endswith('complete'):
#         MPost.update_valid(postinfo.uid)
#     else:
#
#         # 返回当前登录用户的角色相关信息
#         request_id = MRequest.create(role['uid'], postinfo.uid, userinfo.uid)
#
#         # 根据当前角色返回相应状态ID#
#         states = MState.query_by_pro_id(role['uid'])
#         state_arr = []
#         for state in states:
#             state_name = state.name
#             state_arr.append(state_name)
#
#             cur_actions = MTransitionAction.query_by_pro_state(role['uid'], state.uid)
#             for cur_act in cur_actions:
#                 MRequestAction.create(request_id, cur_act['action'], cur_act['transition'])
#
#         act_recs = MTransitionAction.query_by_process(role['uid'])
#
#         act_arr = []
#         for act in act_recs:
#             act_dic = {"act_name": act['name'], "act_uid": act['uid'], "request_id": request_id}
#             act_arr.append(act_dic)
#
#
# else:
#     # 根据当前转换获取下一步状态
#     trans = MTransition.get_by_uid(istrues.transition).get()
#     state = MState.get_by_uid(trans.current_state).get()
#
#     if state.state_type.endswith('complete'):
#         MPost.update_valid(postinfo.uid)
#     else:
#         # 根据状态的流程（角色）获取相关动作
#         act_recs = MTransitionAction.query_by_process(state.process)
#
#         for act in act_recs:
#             act_dic = {"act_name": act['name'], "act_uid": act['uid'], "request_id": istrues.request}
#             act_arr.append(act_dic)


#######################################################################
class State(tornado.web.UIModule):

    def render(self, *args, **kwargs):
        postinfo = kwargs.get('postinfo', '')
        userinfo = kwargs.get('userinfo', '')
        kind = kwargs.get('kind', '9')
        # post_authority = config.post_cfg[kind]['checker']


        #根据post查询最新
        cur_pro=MProcess.query_by_name(postinfo.uid)

        if cur_pro.count() > 0:
            process_id=cur_pro.get().uid

            ##查询当前用户的请求
            request_rec = MRequest.get_by_pro(process_id)



            act_arr = []
            if request_rec:
                cur_state_id = request_rec.current_state
                act_recs = MTransitionAction.query_by_pro_state(process_id,cur_state_id)

                for act in act_recs:
                    print("1" * 50)
                    print(act)
                    act_rec=MAction.get_by_id(act['action']).get()
                    act_dic = {"act_name": act_rec.name, "act_uid": act_rec.uid, "request_id": request_rec.uid}
                    act_arr.append(act_dic)
            else:
                cur_state_id=''



        else:
            # 创建流程
            process_id=MProcess.create(postinfo.uid)
            # 创建动作
            self.test_create_action(process_id, postinfo.uid)


            # 创建状态
            state_dic=self.test_create_state(process_id, postinfo.uid)

            # 创建状态转换
            self.test_create_trans(process_id, state_dic, postinfo.uid)


            # 创建请求
            act_arr,cur_state_id=self.test_create_request(process_id, postinfo.uid,userinfo.uid)

        kwd = {
            'router': config.post_cfg[kind]['router'],
            'kind': kind,
            # 'post_authority': post_authority,
        }

        return self.render_string(
            'modules/post/state.html',
            postinfo=postinfo,
            userinfo=userinfo,
            kwd=kwd,
            action_arr=act_arr,
            cur_state_id=cur_state_id
        )

    def test_create_state(self, process_id, post_id):
        '''
        创建状态TabState
        '''

        state_datas = [
            {'process': process_id, 'name': '开始_{0}'.format(post_id),
             'state_type': 'start_{0}'.format(post_id),
             'description': '每个进程只应该一个。此状态是创建新请求时所处的状态_{0}'.format(post_id)},
            {'process': process_id, 'name': '拒绝_{0}'.format(post_id),
             'state_type': 'denied_{0}'.format(post_id),
             'description': '表示此状态下的任何请求已被拒绝的状态(例如，从未开始且不会被处理)_{0}'.format(post_id)},
            {'process': process_id, 'name': '完成_{0}'.format(post_id),
             'state_type': 'complete_{0}'.format(post_id),
             'description': '表示此状态下的任何请求已正常完成的状态_{0}'.format(post_id)},
            {'process': process_id, 'name': '取消_{0}'.format(post_id),
             'state_type': 'cancelled_{0}'.format(post_id),
             'description': '表示此状态下的任何请求已被取消的状态(例如，工作已开始但尚未完成)_{0}'.format(post_id)},
            {'process': process_id, 'name': '正常_{0}'.format(post_id),
             'state_type': 'normal_{0}'.format(post_id),
             'description': '没有特殊名称的常规状态_{0}'.format(post_id)},

        ]
        state_dic= {}
        for state_data in state_datas:
            state_uid = MState.create(state_data)
            state_dic[state_data['state_type']] = state_uid

        return state_dic
    def test_create_action(self, process_id, post_id):
        '''
        创建动作TabAction
        '''

        action_datas = [
            {'action_type': 'deny_{0}'.format(post_id),
             'name': '拒绝_{0}'.format(post_id), 'description': '操作人将请求应移至上一个状态_{0}'.format(post_id)},
            {'action_type': 'cancel_{0}'.format(post_id),
             'name': '取消_{0}'.format(post_id),
             'description': '操作人将请求应在此过程中移至“已取消”状态_{0}'.format(post_id)},
            {'action_type': 'resolve_{0}'.format(post_id),
             'name': '完成_{0}'.format(post_id),
             'description': '操作人将将请求一直移动到Completed状态_{0}'.format(post_id)},
            {'action_type': 'approve_{0}'.format(post_id),
             'name': '通过_{0}'.format(post_id), 'description': '操作人将请求应移至下一个状态_{0}'.format(post_id)},
            {'action_type': 'restart_{0}'.format(post_id),
             'name': '提交审核_{0}'.format(post_id),
             'description': '操作人将将请求移回到进程中的“开始”状态_{0}'.format(post_id)},

        ]

        action_uids = []
        for act in action_datas:
            act_uid = MAction.create(process_id, act)
            action_uids.append(act_uid)
        assert action_uids

    def test_create_trans(self, process_id, state_dic, post_id):
        '''
         转换Tabtransition
        '''
        if post_id:
            deny = 'deny_' + post_id
            cancel = 'cancel_' + post_id
            resolve = 'resolve_' + post_id
            restart = 'restart_' + post_id
            approve = 'approve_' + post_id

            act_deny = MAction.get_by_action_type(deny).uid
            act_cancel = MAction.get_by_action_type(cancel).uid
            act_resolve = MAction.get_by_action_type(resolve).uid
            act_restart = MAction.get_by_action_type(restart).uid
            act_approve = MAction.get_by_action_type(approve).uid

            trans = [
                # 状态：“开始”对应的“拒绝”，“完成”，“取消”
                {'current_state': state_dic['start_{}'.format(post_id)],
                 'next_state': state_dic['denied_{}'.format(post_id)], 'act_id': act_deny},
                {'current_state': state_dic['start_{}'.format(post_id)],
                 'next_state': state_dic['complete_{}'.format(post_id)], 'act_id': act_approve},
                {'current_state': state_dic['start_{}'.format(post_id)],
                 'next_state': state_dic['cancelled_{}'.format(post_id)], 'act_id': act_cancel},

                # 状态：“完成”对应的“正常”
                {'current_state': state_dic['complete_{}'.format(post_id)],
                 'next_state': state_dic['normal_{}'.format(post_id)], 'act_id': act_resolve},

                # 状态：“取消”对应的“拒绝”，“完成”
                {'current_state': state_dic['cancelled_{}'.format(post_id)],
                 'next_state': state_dic['denied_{}'.format(post_id)], 'act_id': act_deny},
                {'current_state': state_dic['cancelled_{}'.format(post_id)],
                 'next_state': state_dic['complete_{}'.format(post_id)], 'act_id': act_approve},

                # 状态：“拒绝”对应的“开始”
                {'current_state': state_dic['denied_{}'.format(post_id)],
                 'next_state': state_dic['start_{}'.format(post_id)], 'act_id': act_restart},

            ]

            for tran in trans:
                tran_id = MTransition.create(process_id, tran['current_state'], tran['next_state'])

                # 创建转换动作
                self.test_create_transaction(tran_id, tran['act_id'])

            # assert True

    def test_create_transaction(self, trans_id, actid):
        '''
       转换动作TransitionAction
        '''

        trans_act = MTransitionAction.create(trans_id, actid)
        # assert trans_act

    def test_create_request(self, process_id, post_id,user_id):
        '''
        创建请求以及请求对应状态的相关动作
        '''

        # 获取“开始”状态ID

        state_type = 'start_{0}'.format(post_id)
        cur_state = MState.get_by_state_type(state_type)
        if cur_state:
            # 创建请求
            req_id = MRequest.create(process_id, post_id, user_id, cur_state.uid)


            # 创建请求操作
            cur_actions = MTransitionAction.query_by_pro_state(process_id, cur_state.uid)
            act_arr=[]
            for cur_act in cur_actions:
                MRequestAction.create(req_id, cur_act['action'], cur_act['transition'])
                act=MAction.get_by_id(cur_act['action']).get()
                if act.action_type.startswith('restart'):
                    act_arr.append({"act_name": act.name, "act_uid": cur_act['action'], "request_id": req_id})
            return act_arr,cur_state.uid

    def test_request_action(self, process_id, cur_state_id,post_id):
        '''
        进行请求操作
        '''

        request_id = MRequest.get_by_pro_state(process_id, cur_state_id)

        act_type = 'approve_{0}'.format(post_id)
        cur_act = MAction.get_by_action_type(act_type)
        print("1" * 50)
        print(request_id)
        if cur_act:
            print("2" * 50)
            print(cur_act.uid)
            print(request_id)
            # 提交的Action与其中一个（is_active = true）的活动RequestActions匹配，设置 is_active = false 和 is_completed = true
            reqact = MRequestAction.get_by_action_request(cur_act.uid, request_id)
            print("3" * 50)
            if reqact:
                if reqact.is_active:
                    # 更新操作动态
                    print("gengxin")
                    MRequestAction.update_by_action(cur_act.uid, request_id)
                # 查询该请求中该转换的所有动作是否都为True
                istrues = MRequestAction.query_by_request_trans(request_id, reqact.transition).get()
                print(istrues)
                if istrues.is_complete:
                    # 禁用该请求下其它动作
                    MRequestAction.update_by_action_reqs(cur_act.uid, request_id)
                    # 转到下一状态
                    trans = MTransition.get_by_uid(reqact.transition).get()
                    new_state = MState.get_by_uid(trans.next_state).get()
                    if new_state.state_type.startswith('normal_'):
                        print("完成" * 5)
                        MPost.update_valid(post_id)

                    else:
                        act_arr = []
                        acts = MTransitionAction.query_by_pro_state(process_id, new_state.uid)
                        for act in acts:
                            act_arr.append({'trans': act['transition'], 'act': act['action']})
                        dics = {'new_state_id': new_state.uid, 'new_actarr': act_arr}
                        print("4" * 50)
                        print(dics)


class Check_pager(tornado.web.UIModule):
    '''
    审核翻页
    '''

    def render(self, *args, **kwargs):
        current = int(args[0])
        state = kwargs.get('state', '')
        kind = kwargs.get('kind', '9')

        num_of_cat = MPost.count_of_certain_by_state(state, kind)

        tmp_page_num = int(num_of_cat / config.CMS_CFG['list_num'])

        page_num = (
            tmp_page_num
            if abs(tmp_page_num - num_of_cat / config.CMS_CFG['list_num']) < 0.1
            else tmp_page_num + 1
        )

        kwd = {
            'page_home': current > 1,
            'page_end': current < page_num,
            'page_pre': current > 1,
            'page_next': current < page_num,
            'kind': kind,
        }

        return self.render_string(
            'modules/post/check_pager.html',
            kwd=kwd,
            pager_num=page_num,
            page_current=current,
            state=state,
        )


class Check_username_pager(tornado.web.UIModule):
    '''
    审核翻页
    '''

    def render(self, *args, **kwargs):
        current = int(args[0])
        username = kwargs.get('username', '')
        state = kwargs.get('sate', '0000')
        kind = kwargs.get('kind', '9')

        num_of_cat = MPost.count_of_certain_by_username(username, state, kind)

        tmp_page_num = int(num_of_cat / config.CMS_CFG['list_num'])

        page_num = (
            tmp_page_num
            if abs(tmp_page_num - num_of_cat / config.CMS_CFG['list_num']) < 0.1
            else tmp_page_num + 1
        )

        kwd = {
            'page_home': current > 1,
            'page_end': current < page_num,
            'page_pre': current > 1,
            'page_next': current < page_num,
            'kind': kind,
        }

        return self.render_string(
            'modules/post/check_username_pager.html',
            kwd=kwd,
            pager_num=page_num,
            page_current=current,
            state=state,
            username=username,
        )
