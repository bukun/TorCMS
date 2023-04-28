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
from torcms.model.state_model import MState, MTransition, MRequest, MAction, MRequestAction, \
    MTransitionAction
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

class State(tornado.web.UIModule):
    '''
    todo：点击通过，拒绝，取消后应该提示已通过，已取消，已拒绝
    '''
    def render(self, *args, **kwargs):
        postinfo = kwargs.get('postinfo', '')
        userinfo = kwargs.get('userinfo', '')
        kind = kwargs.get('kind', '9')
        post_authority = config.post_cfg[kind]['checker']

        ##查询当前用户的请求
        request_rec = MRequest.get_id_by_username(postinfo.uid, postinfo.user_name)


        act_arr = []
        if request_rec:

            # 查询该请求中该转换的所有动作是否都为True
            istrues = MRequestAction.query_by_request(request_rec.uid).get()

            if istrues.is_complete:

                # 转到下一状态
                trans = MTransition.get_by_uid(istrues.transition).get()
                state = MState.get_by_uid(trans.next_state).get()

                print(trans.uid)

                if state.state_type.endswith('complete'):
                    MPost.update_valid(postinfo.uid)

                else:

                    # 返回当前登录用户的角色相关信息
                    role = MStaff2Role.get_role_by_uid(userinfo.uid).get()
                    if role:

                        request_id = MRequest.create(role['uid'], postinfo.uid, userinfo.uid)

                        # 根据当前角色返回相应状态ID#
                        states = MState.query_by_pro_id(role['uid'])
                        state_arr = []
                        for state in states:
                            state_name = state.name
                            state_arr.append(state_name)

                            cur_actions = MTransitionAction.query_by_action_state(role['uid'], state.uid)
                            for cur_act in cur_actions:
                                MRequestAction.create(request_id, cur_act['action'], cur_act['transition'])

                        act_recs = MTransitionAction.query_by_process(role['uid'])

                        act_arr = []
                        for act in act_recs:
                            act_dic = {"act_name": act['name'], "act_uid": act['uid'], "request_id":  request_id}
                            act_arr.append(act_dic)
                    else:
                        act_arr = [{"act_name": "Waiting for review", "act_uid": "", "request_id":  ''}]
                        request_id = ''
                    # 以上创建步骤已完成
                    print("+" * 50)
                    print(act_arr)

            else:
                #根据当前转换获取下一步状态
                trans = MTransition.get_by_uid(istrues.transition).get()
                state = MState.get_by_uid(trans.current_state).get()


                if state.state_type.endswith('complete'):
                    MPost.update_valid(postinfo.uid)
                else:
                    #根据状态的流程（角色）获取相关动作
                    act_recs = MTransitionAction.query_by_process(state.process)


                    for act in act_recs:

                        act_dic = {"act_name": act['name'], "act_uid": act['uid'], "request_id":  istrues.request}
                        act_arr.append(act_dic)



        kwd = {
            'router': config.post_cfg[kind]['router'],
            'kind': kind,
            'post_authority': post_authority,
        }

        return self.render_string(
            'modules/post/state.html',
            postinfo=postinfo,
            userinfo=userinfo,
            kwd=kwd,
            action_arr=act_arr
        )


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
