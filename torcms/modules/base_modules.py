# -*- coding:utf-8 -*-

'''
Define the basic modules for TorCMS.
'''

from math import ceil as math_ceil

import bs4
import tornado.escape
import tornado.web

import config
from torcms.core.tool.whoosh_tool import YunSearch
from torcms.core.tools import logger
from torcms.model.category_model import MCategory
from torcms.model.collect_model import MCollect
from torcms.model.entity2user_model import MEntity2User
from torcms.model.entity_model import MEntity
from torcms.model.label_model import MPost2Label
from torcms.model.link_model import MLink
from torcms.model.post2catalog_model import MPost2Catalog
from torcms.model.post_model import MPost
from torcms.model.reply2user_model import MReply2User
from torcms.model.user_model import MUser
from torcms.model.wiki_model import MWiki
from torcms.model.reply_model import MReply


class ShowPage(tornado.web.UIModule):
    '''
    Get page info by page_id.
    '''

    def render(self, *args, **kwargs):
        '''
        '''
        page_id = kwargs['page_id']
        userinfo = kwargs.get('userinfo', None)
        count = kwargs.get('count', 0)
        page = MWiki.get_by_uid(page_id)
        kwd = {
            'uid': page_id,
            'count': count
        }
        if page:
            out_str = self.render_string('modules/show_page.html',

                                         postinfo=page,
                                         userinfo=userinfo,
                                         kwd=kwd)
        else:
            out_str = '<a href="/page/{0}">{0}</a>'.format(page_id)
        return out_str


class PostListOfTag(tornado.web.UIModule):
    def render(self, *args, **kwargs):
        tagid = args[0]
        posts = MPost.query_by_tag(tagid, kind='5')
        outstr = ''
        for postinfo in posts:
            tmpl = '''<li class ="list-group-item" ><a href="/course/{uid}">{title}</a></li>
            '''.format(title=postinfo.title, uid=postinfo.uid)
            outstr = outstr + tmpl
        return outstr


class PostLabels(tornado.web.UIModule):
    '''
    Show the labels of the post.
    '''

    def render(self, *args, **kwargs):
        postinfo = kwargs.get('postinfo', None)
        if postinfo:
            tag_info = filter(lambda x: not x.tag_name.startswith('_'),
                              MPost2Label.get_by_uid(postinfo.uid).objects())
            idx = 1
            outstr = '<span class="post_label">'
            for tag in tag_info:
                outstr += '''<a href="/label/{kind}/{tag_uid}"
                    class ="app_label tag{index}"> {tag_name} </a>
                    '''.format(tag_uid=tag.tag_id,
                               kind=postinfo.kind,
                               tag_name=tag.tag_name,
                               index=idx)
                idx += 1
            return outstr + '</span>'
        return ''


class GetFooter(tornado.web.UIModule):
    '''
    Render footer.
    '''

    def render(self, *args, **kwargs):
        logger.info('Init footer')
        all_cats = MCategory.query_all()
        kwd = {
            'cats': all_cats,
        }
        return self.render_string('modules/post/menu.html',
                                  kwd=kwd)


class PreviousPostLink(tornado.web.UIModule):
    '''
    Link for the previous post link.
    '''

    def render(self, *args, **kwargs):
        current_id = args[0]
        prev_record = MPost.get_previous_record(current_id)
        if prev_record:
            kwd = {
                'uid': prev_record.uid,
            }
            return self.render_string('modules/post/pre_page.html', kwd=kwd)
        return self.render_string('modules/post/last_page.html')


class NextPostLink(tornado.web.UIModule):
    '''
    Link for the next post link.
    '''

    def render(self, *args, **kwargs):
        current_id = args[0]
        next_record = MPost.get_next_record(current_id)
        if next_record:
            kwd = {
                'uid': next_record.uid,
            }
            return self.render_string('modules/post/next_page.html', kwd=kwd)
        return self.render_string('modules/post/newest_page.html')


class PostMostView(tornado.web.UIModule):
    '''
    list of most viewd posts.
    '''

    def render(self, num, with_date=True, with_catalog=True, kind='1'):
        kwd = {
            'with_date': with_date,
            'with_catalog': with_catalog,
            'router': config.router_post['1'],
            'kind': kind
        }

        return self.render_string('modules/post/post_list.html',
                                  recs=MPost.query_most(num=num, kind=kind),
                                  kwd=kwd)


class PostRandom(tornado.web.UIModule):
    '''
    return some posts randomly.
    '''

    def render(self, num, with_date=True, with_catalog=True, kind='1'):
        kwd = {
            'with_date': with_date,
            'with_catalog': with_catalog,
            'router': config.router_post['1']
        }
        return self.render_string('modules/post/post_list.html',
                                  recs=MPost.query_random(num=num, kind=kind),
                                  kwd=kwd)


class PostCatRandom(tornado.web.UIModule):
    '''
    return some posts randomly of certain category.
    '''

    def render(self, cat_id, num, with_date=True, with_catalog=True):
        kwd = {
            'with_date': with_date,
            'with_catalog': with_catalog,
            'router': config.router_post['1'],
        }
        return self.render_string('modules/post/post_list.html',
                                  recs=MPost.query_cat_random(cat_id, limit=num),
                                  kwd=kwd)


class PostRecentMostView(tornado.web.UIModule):
    '''
    return some posts most viewed recently.
    '''

    def render(self, num, recent, with_date=True, with_catalog=True):
        kwd = {
            'with_date': with_date,
            'with_catalog': with_catalog,
            'router': config.router_post['1'],
        }
        return self.render_string('modules/post/post_list.html',
                                  recs=MPost.query_recent_most(num, recent),
                                  kwd=kwd)


class CategoryOf(tornado.web.UIModule):
    '''
    return the categories which uid starts with certain string.
    '''

    def render(self, *args, **kwargs):
        uid_with_str = args[0]
        return self.render_string('modules/post/catalog_of.html',
                                  recs=MCategory.query_uid_starts_with(uid_with_str))


class PostCategoryOf(tornado.web.UIModule):
    '''
    The catalog of the post.
    '''

    def render(self, uid_with_str, slug=False, order=False, glyph=''):
        curinfo = MCategory.get_by_uid(uid_with_str)
        sub_cats = MCategory.query_sub_cat(uid_with_str)
        kwd = {
            'glyph': glyph
        }
        if slug:
            return self.render_string('modules/post/post_catalog_slug.html',
                                      pcatinfo=curinfo,
                                      sub_cats=sub_cats,
                                      recs=sub_cats,
                                      order=order,
                                      kwd=kwd)
        else:
            return self.render_string('modules/info/catalog_of.html',
                                      pcatinfo=curinfo,
                                      sub_cats=sub_cats,
                                      recs=sub_cats,
                                      kwd=kwd)


class PostRecent(tornado.web.UIModule):
    '''
    return the post of recent.
    '''

    def render(self, num=10, with_catalog=True, with_date=True, kind='1'):
        kwd = {
            'with_date': with_date,
            'with_catalog': with_catalog,
            'router': config.router_post['1'],
            'kind': kind
        }
        return self.render_string('modules/post/post_list.html',
                                  recs=MPost.query_recent(num, kind=kind),

                                  kwd=kwd)


class LinkList(tornado.web.UIModule):
    '''
    return the list of links.
    '''

    def render(self, *args, **kwargs):
        num = kwargs['num'] if 'num' in kwargs else 10
        return self.render_string('modules/post/link_list.html',
                                  recs=MLink.query_link(num))


class PostCategoryRecent(tornado.web.UIModule):
    '''
    The reccent posts of certain category.
    '''

    def render(self, cat_id, label=None, num=10, with_catalog=True, with_date=True, glyph='',
               **kwargs):

        is_spa = kwargs.get('spa', False)

        catinfo = MCategory.get_by_uid(cat_id)
        if catinfo.pid == '0000':
            subcats = MCategory.query_sub_cat(cat_id)
            sub_cat_ids = [x.uid for x in subcats]
            recs = MPost.query_total_cat_recent(sub_cat_ids, label=label, num=num,
                                                kind=catinfo.kind)

        else:
            recs = MPost.query_cat_recent(cat_id, label=label, num=num, kind=catinfo.kind)

        kwd = {
            'with_catalog': with_catalog,
            'with_category': with_catalog,
            'with_date': with_date,
            'router': config.router_post[catinfo.kind],
            'glyph': glyph,
            'spa': is_spa
        }
        return self.render_string('modules/post/post_list.html',
                                  recs=recs,

                                  kwd=kwd)


class ShowoutRecent(tornado.web.UIModule):
    '''
    return posts of recent for showing out.
    '''

    def render(self, cat_id, kind, **kwargs):
        num = kwargs.get('num', 10)

        width = kwargs.get('width', 160)
        height = kwargs.get('height', 120)
        with_catalog = kwargs.get('with_catalog', True)
        with_date = kwargs.get('with_date', True)

        kwd = {
            'with_catalog': with_catalog,
            'with_date': with_date,
            'width': width,
            'height': height,
        }

        return self.render_string('modules/post/showout_list.html',
                                  recs=MPost.query_cat_recent(cat_id, num=num, kind=kind),
                                  kwd=kwd)


class SiteUrl(tornado.web.UIModule):
    '''
    return the url of the site.
    '''

    def render(self, *args, **kwargs):
        return config.SITE_CFG['site_url']


class SiteTitle(tornado.web.UIModule):
    '''
    return the title of the site.
    '''

    def render(self, *args, **kwargs):
        return ''


class TheCategory(tornado.web.UIModule):
    '''
    return the category according to the id of post.
    '''

    def render(self, post_id, order=False):
        if order:
            tmpl_str = '''<a href="/catalog/{0}">{1}</a>'''
        else:
            tmpl_str = '''<a href="/category/{0}">{1}</a>'''

        # print('=' * 10)
        # for uu in MPost2Catalog().query_by_entity_uid(post_id):
        #     print(dir(uu.as_entity()))
        format_arr = [tmpl_str.format(uu.tag_slug, uu.tag_name) for uu in
                      MPost2Catalog().query_by_entity_uid(post_id).objects()]
        return ', '.join(format_arr)


class ListCategories(tornado.web.UIModule):
    '''
    list categories.
    '''

    def render(self, cat_id, list_num):
        recs = MPost.query_cat_recent(cat_id, num=list_num)
        out_str = ''
        for rec in recs:
            tmp_str = '''<li><a href="/{0}">{1}</a></li>'''.format(
                rec.title,
                rec.title
            )
            out_str += tmp_str
        return out_str


class GenerateAbstract(tornado.web.UIModule):
    '''
    translate html to text, and return 130 charactors.
    '''

    def render(self, *args, **kwargs):
        html_str = args[0]
        tmp_str = bs4.BeautifulSoup(tornado.escape.xhtml_unescape(html_str), "html.parser")
        return tmp_str.get_text()[:130] + '....'


# Todo: should be deleted.
class GenerateDescription(tornado.web.UIModule):
    '''
    Just as GenerateAbstract
    '''

    def render(self, *args, **kwargs):
        html_str = args[0]
        tmp_str = bs4.BeautifulSoup(tornado.escape.xhtml_unescape(html_str), "html.parser")
        return tmp_str.get_text()[:100]


class CopyRight(tornado.web.UIModule):
    '''
    show TorCMS copy right.
    '''

    def render(self, *args, **kwargs):
        return '''<span>Build on
        <a href="https://github.com/bukun/TorCMS" target="_blank">TorCMS</a>.</span>'''


class PostTags(tornado.web.UIModule):
    '''
    show tags of the post.
    '''

    def render(self, *args, **kwargs):
        uid = args[0]
        kind = args[1]
        out_str = ''
        idx = 1
        for tag_info in MPost2Catalog.query_by_entity_uid(uid, kind=kind).objects():
            tmp_str = '<a href="/category/{0}" class="tag{1}">{2}</a>'.format(
                tag_info.tag_slug,
                idx,
                tag_info.tag_name)
            out_str += tmp_str
            idx += 1
        return out_str


class MapTags(tornado.web.UIModule):
    '''
    show tags of the map.
    '''

    def render(self, *args, **kwargs):
        uid = args[0]
        out_str = ''
        idx = 1
        for tag_info in MPost2Catalog.query_by_entity_uid(uid, kind='m').objects():
            tmp_str = '<a href="/tag/{0}" class="tag{1}">{2}</a>'.format(
                tag_info.tag_slug,
                idx,
                tag_info.tag_name)
            out_str += tmp_str
            idx += 1
        return out_str


class ModuleCatMenu(tornado.web.UIModule):
    '''

    '''

    def render(self, with_count=True):
        kwd = {
            'cats': MCategory.query_all(by_count=True),
            'with_count': with_count,
        }
        return self.render_string('modules/post/menu_post.html',
                                  kwd=kwd)


class ToplineModule(tornado.web.UIModule):
    '''

    '''

    def render(self, *args, **kwargs):
        return self.render_string('modules/widget/topline.html')


class CategoryPager(tornado.web.UIModule):
    '''
    pager of category
    '''

    def render(self, *args, **kwargs):
        cat_slug = args[0]
        current = int(args[1])
        # cat_slug 分类
        # current 当前页面
        tag = kwargs['tag'] if 'tag' in kwargs else ""

        cat_rec = MCategory.get_by_slug(cat_slug)
        num_of_cat = MPost2Catalog.count_of_certain_category(cat_rec.uid, tag=tag)

        pager_cnt = int(num_of_cat / config.CMS_CFG['list_num'])

        page_num = (pager_cnt if abs(pager_cnt - num_of_cat / config.CMS_CFG['list_num']) < 0.1
                    else pager_cnt + 1)

        kwd = {
            'page_home': False if current <= 1 else True,
            'page_end': False if current >= page_num else True,
            'page_pre': False if current <= 1 else True,
            'page_next': False if current >= page_num else True,
            'tag': tag,
        }

        return self.render_string('modules/post/catalog_pager.html',
                                  kwd=kwd,
                                  cat_slug=cat_slug,
                                  pager_num=page_num,
                                  page_current=current)


class CollectPager(tornado.web.UIModule):
    '''
    pager of category
    '''

    def render(self, *args, **kwargs):
        user_id = args[0]
        current = int(args[1])
        # cat_slug 分类
        # current 当前页面

        the_count = MCollect.count_of_user(user_id)

        pager_count = int(the_count / config.CMS_CFG['list_num'])

        page_num = (pager_count if abs(pager_count - the_count / config.CMS_CFG['list_num']) < 0.1
                    else pager_count + 1)

        kwd = {
            'page_home': False if current <= 1 else True,
            'page_end': False if current >= page_num else True,
            'page_pre': False if current <= 1 else True,
            'page_next': False if current >= page_num else True,
        }

        return self.render_string('modules/post/collect_pager.html',
                                  kwd=kwd,
                                  pager_num=page_num,
                                  page_current=current)


class InfoLabelPager(tornado.web.UIModule):
    '''
    Pager for info label.
    '''

    def render(self, *args, **kwargs):
        tag_slug = args[0]
        current = int(args[1])

        cat_rec = MPost.query_by_tagname(tag_slug)

        pager_count = int(cat_rec.count() / config.CMS_CFG['list_num'])
        page_num = (
            pager_count if abs(pager_count - cat_rec.count() / config.CMS_CFG['list_num']) < 0.1
            else pager_count + 1)

        kwd = {
            'page_home': False if current <= 1 else True,
            'page_end': False if current >= page_num else True,
            'page_pre': False if current <= 1 else True,
            'page_next': False if current >= page_num else True,
        }

        return self.render_string('modules/post/info_label_pager.html',
                                  kwd=kwd,
                                  cat_slug=tag_slug,
                                  pager_num=page_num,
                                  page_current=current)


class LabelPager(tornado.web.UIModule):
    '''
    Pager for label.
    '''

    def render(self, *args, **kwargs):
        kind = args[0]
        tag_slug = args[1]
        current = int(args[2])

        pager_count = int(MPost2Label.total_number(tag_slug, kind) / config.CMS_CFG['list_num'])
        page_num = (pager_count if abs(
            pager_count - MPost2Label.total_number(tag_slug, kind) / config.CMS_CFG[
                'list_num']) < 0.1 else pager_count + 1)
        kwd = {
            'page_home': False if current <= 1 else True,
            'page_end': False if current >= page_num else True,
            'page_pre': False if current <= 1 else True,
            'page_next': False if current >= page_num else True,
        }

        return self.render_string('modules/post/label_pager.html',
                                  kwd=kwd,
                                  cat_slug=tag_slug,
                                  pager_num=page_num,
                                  page_current=current,
                                  kind=kind)


class TagPager(tornado.web.UIModule):
    '''
    Pager for tag.
    '''

    def render(self, *args, **kwargs):
        tag_slug = args[0]
        current = int(args[1])
        taginfo = MCategory.get_by_slug(tag_slug)
        num_of_tag = MPost2Catalog.count_of_certain_category(taginfo.uid)
        pager_count = int(math_ceil(num_of_tag / config.CMS_CFG['list_num']))
        page_num = (pager_count if abs(pager_count - num_of_tag / config.CMS_CFG['list_num']) < 0.1
                    else pager_count + 1)

        kwd = {
            'page_home': False if current <= 1 else True,
            'page_end': False if current >= page_num else True,
            'page_pre': False if current <= 1 else True,
            'page_next': False if current >= page_num else True,
        }

        return self.render_string('modules/post/tag_pager.html',
                                  kwd=kwd,
                                  cat_slug=tag_slug,
                                  pager_num=page_num,
                                  page_current=current)


class SearchPager(tornado.web.UIModule):
    '''
    Pager for search result.
    '''

    def render(self, *args, **kwargs):
        ysearch = YunSearch()
        catid = args[0]
        tag_slug = args[1]
        current = int(args[2])
        res_all = ysearch.get_all_num(tag_slug, catid=catid)
        pager_count = int(res_all / config.CMS_CFG['list_num'])
        page_num = (pager_count if abs(pager_count - res_all / config.CMS_CFG['list_num']) < 0.1
                    else pager_count + 1)
        kwd = {
            'page_home': False if current <= 1 else True,
            'page_end': False if current >= page_num else True,
            'page_pre': False if current <= 1 else True,
            'page_next': False if current >= page_num else True,
        }

        return self.render_string('modules/post/search_pager.html',
                                  kwd=kwd,
                                  cat_slug=tag_slug,
                                  catid=catid,
                                  pager_num=page_num,
                                  page_current=current)


class AppTitle(tornado.web.UIModule):
    '''
    search widget. Simple searching. searching for all.
    '''

    def render(self, *args, **kwargs):
        uid = args[0]
        rec = MPost.get_by_uid(uid=uid)
        return rec.title if rec else None


class EntityList(tornado.web.UIModule):
    '''
    search widget. Simple searching. searching for all.
    '''

    def render(self, kind, cur_p=''):
        if cur_p == '':
            current_page_number = 1
        else:
            current_page_number = int(cur_p)

        current_page_number = 1 if current_page_number < 1 else current_page_number
        kwd = {
            'current_page': current_page_number
        }

        recs = MEntity.get_by_kind(kind=kind, current_page_num=current_page_number)

        return self.render_string('modules/post/entity_list.html',
                                  kwd=kwd,
                                  rec=recs)


class EntityPager(tornado.web.UIModule):
    '''
    Pager for search result.
    '''

    def render(self, *args, **kwargs):
        current = int(args[0])

        pager_count = int(MEntity.total_number() / config.CMS_CFG['list_num'])
        page_num = (
            pager_count if abs(
                pager_count - MEntity.total_number() / config.CMS_CFG['list_num']) < 0.1
            else pager_count + 1)
        kwd = {
            'page_home': False if current <= 1 else True,
            'page_end': False if current >= page_num else True,
            'page_pre': False if current <= 1 else True,
            'page_next': False if current >= page_num else True,
        }

        return self.render_string('modules/post/entity_pager.html',
                                  kwd=kwd,
                                  pager_num=page_num,
                                  page_current=current)


class Entity2UserPager(tornado.web.UIModule):
    '''
    Pager for search result.
    '''

    def render(self, *args, **kwargs):
        current = int(args[0])
        user_id = kwargs.get('userid', None)

        pager_count = int(MEntity2User.total_number_by_user(user_id) / config.CMS_CFG['list_num'])
        page_num = (pager_count if abs(
            pager_count - MEntity2User.total_number_by_user(user_id) / config.CMS_CFG['list_num']) < 0.1
                    else pager_count + 1)
        kwd = {
            'page_home': False if current <= 1 else True,
            'page_end': False if current >= page_num else True,
            'page_pre': False if current <= 1 else True,
            'page_next': False if current >= page_num else True,
        }

        return self.render_string('modules/post/entity_user_download_pager.html',
                                  kwd=kwd,
                                  user_id=user_id,
                                  pager_num=page_num,
                                  page_current=current)


class Entity2Pager(tornado.web.UIModule):
    '''
    Pager for search result.
    '''

    def render(self, *args, **kwargs):
        current = int(args[0])
        user_id = kwargs.get('userid', None)

        pager_count = int(MEntity2User.total_number() / config.CMS_CFG['list_num'])
        page_num = (pager_count if abs(
            pager_count - MEntity2User.total_number() / config.CMS_CFG['list_num']) < 0.1
                    else pager_count + 1)
        kwd = {
            'page_home': False if current <= 1 else True,
            'page_end': False if current >= page_num else True,
            'page_pre': False if current <= 1 else True,
            'page_next': False if current >= page_num else True,
        }

        return self.render_string('modules/post/entity_download_pager.html',
                                  kwd=kwd,
                                  user_id=user_id,
                                  pager_num=page_num,
                                  page_current=current)


# class Entity_path(tornado.web.UIModule):
#     '''
#     Pager for search result.
#     '''
#
#     def render(self, enti_id):
#         rec = MEntity.get_by_uid(enti_id)
#
#         return self.render_string('modules/post/entity_path.html',
#                                   rec=rec)


class UserName(tornado.web.UIModule):
    '''
    Pager for search result.
    '''

    def render(self, *args, **kwargs):
        user_id = args[0]
        rec = MUser.get_by_uid(user_id)

        return self.render_string('modules/post/user_name.html',
                                  rec=rec)


class ReplyPostById(tornado.web.UIModule):
    '''
    Pager for search result.
    '''

    def render(self, post_id, reply_uid):
        try:
            rec = MPost.get_by_uid(post_id)
            return rec.title
        except:
            # todo:进入评论列表页面后显示None，再刷新才会删除不存在post的评论
            MReply2User.delete(reply_uid)


# Todo: Should to be reviewed.
class CategoryBySlug(tornado.web.UIModule):
    '''
    catalog 列表页 面包屑导航
    '''

    def render(self, *args, **kwargs):
        slug = args[0]
        rec = MCategory.get_by_slug(slug)

        par = MCategory.get_by_uid(rec.pid)
        if rec.uid.endswith('00'):
            tmp_str = '<li class="active">{0}</li>'.format(
                rec.name
            )

        else:
            tmp_str = '<li><a href="/catalog/{0}">{1}</a></li><li class="active">{2}</li>'.format(
                par.slug,
                par.name,
                rec.name
            )
        return tmp_str


class Collect(tornado.web.UIModule):
    '''
添加收藏模块
    '''

    def render(self, *args, **kwargs):
        user_id = args[0]
        post_id = args[1]
        user_collect = MCollect.get_by_signature(user_id, post_id)
        return self.render_string('modules/widget/collect.html', user_collect=user_collect)


class UserCollect(tornado.web.UIModule):
    '''
    用户收藏列表
    '''

    def render(self, *args, **kwargs):
        user_id = kwargs.get('user_id', args[0])
        kind = kwargs.get('kind', args[1])
        num = kwargs.get('num', args[2] if len(args) > 2 else 6)
        with_tag = kwargs.get('with_tag', False)
        glyph = kwargs.get('glyph', '')

        all_cats = MCollect.query_pager_by_userid(user_id, kind, num).objects()
        kwd = {
            'with_tag': with_tag,
            'glyph': glyph
        }
        return self.render_string('modules/widget/user_collect.html',
                                  recs=all_cats,
                                  kwd=kwd)


class Admin_Post_pager(tornado.web.UIModule):
    '''
    pager of kind
    '''

    def render(self, *args, **kwargs):
        kind = args[0]
        current = int(args[1])
        # kind
        # current 当前页面

        num_of_cat = MPost.count_of_certain_kind(kind)

        tmp_page_num = int(num_of_cat / config.CMS_CFG['list_num'])

        page_num = (tmp_page_num if abs(tmp_page_num - num_of_cat / config.CMS_CFG['list_num']) < 0.1
                    else tmp_page_num + 1)

        kwd = {
            'page_home': False if current <= 1 else True,
            'page_end': False if current >= page_num else True,
            'page_pre': False if current <= 1 else True,
            'page_next': False if current >= page_num else True,
        }

        return self.render_string('modules/admin/post_pager.html',
                                  kwd=kwd,
                                  pager_num=page_num,
                                  kind=kind,
                                  page_current=current)


class Admin_Page_pager(tornado.web.UIModule):
    '''
    pager of kind
    '''

    def render(self, *args, **kwargs):
        kind = args[0]
        current = int(args[1])
        # kind
        # current 当前页面

        num_of_cat = MWiki.count_of_certain_kind(kind)

        tmp_page_num = int(num_of_cat / config.CMS_CFG['list_num'])

        page_num = (tmp_page_num if abs(tmp_page_num - num_of_cat / config.CMS_CFG['list_num']) < 0.1
                    else tmp_page_num + 1)

        kwd = {
            'page_home': False if current <= 1 else True,
            'page_end': False if current >= page_num else True,
            'page_pre': False if current <= 1 else True,
            'page_next': False if current >= page_num else True,
        }

        return self.render_string('modules/admin/page_pager.html',
                                  kwd=kwd,
                                  pager_num=page_num,
                                  kind=kind,
                                  page_current=current)


class Admin_reply_pager(tornado.web.UIModule):
    '''
    pager of kind
    '''

    def render(self, *args, **kwargs):
        current = int(args[0])
        # kind
        # current 当前页面

        num_of_cat = MReply.count_of_certain()

        tmp_page_num = int(num_of_cat / config.CMS_CFG['list_num'])

        page_num = (tmp_page_num if abs(tmp_page_num - num_of_cat / config.CMS_CFG['list_num']) < 0.1
                    else tmp_page_num + 1)

        kwd = {
            'page_home': False if current <= 1 else True,
            'page_end': False if current >= page_num else True,
            'page_pre': False if current <= 1 else True,
            'page_next': False if current >= page_num else True,
        }

        return self.render_string('modules/admin/reply_pager.html',
                                  kwd=kwd,
                                  pager_num=page_num,
                                  page_current=current)
