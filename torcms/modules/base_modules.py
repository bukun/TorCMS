# -*- coding:utf-8 -*-

'''
Define the basic modules for TorCMS.
'''

from math import ceil as math_ceil
import bs4
import tornado.web
import tornado.escape
from torcms.model.post_model import MPost
from torcms.model.link_model import MLink
from torcms.model.post2catalog_model import MPost2Catalog
from torcms.model.category_model import MCategory
from torcms.model.label_model import MPost2Label
from torcms.model.wiki_model import MWiki
from torcms.model.collect_model import MCollect
from torcms.core.tool.whoosh_tool import YunSearch
from torcms.core.tools import logger
import config


class ShowPage(tornado.web.UIModule):
    '''
    Get page info by page_id.
    '''

    def render(self, *args, **kwargs):
        '''
        '''
        page_id = kwargs['page_id']
        userinfo = kwargs['userinfo'] if 'userinfo' in kwargs else None
        count = kwargs['count'] if 'count' in kwargs else 0
        page = MWiki.get_by_uid(page_id)
        kwd = {
            'uid': page_id,
            'count': count
        }
        if page:
            return self.render_string('modules/show_page.html',
                                      unescape=tornado.escape.xhtml_unescape,
                                      postinfo=page,
                                      userinfo=userinfo,
                                      kwd=kwd)
        else:
            return '<a href="/page/{0}">{0}</a>'.format(page_id)


class PostLabels(tornado.web.UIModule):
    '''
    Show the labels of the post.
    '''

    def render(self, postinfo=None):
        if postinfo:
            tag_info = MPost2Label.get_by_uid(postinfo.uid).naive()
            idx = 1
            outstr = '<span class="post_label">'
            for tag in tag_info:
                outstr += '''<a href = "/label/{kind}/{tag_uid}"
                    class ="app_label tag{index}" > {tag_name} </a>
                    '''.format(tag_uid=tag.tag_id,
                               kind=postinfo.kind,
                               tag_name=tag.tag_name,
                               index=idx)
                idx += 1
            return outstr + '</span>'
        else:
            return ''


class GetFooter(tornado.web.UIModule):
    '''
    Render footer.
    '''

    def render(self):
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

    def render(self, current_id):
        prev_record = MPost.get_previous_record(current_id)
        if prev_record is None:
            return self.render_string('modules/post/last_page.html')
        else:
            kwd = {
                'uid': prev_record.uid,
            }
            return self.render_string('modules/post/pre_page.html', kwd=kwd)


class NextPostLink(tornado.web.UIModule):
    '''
    Link for the next post link.
    '''

    def render(self, current_id):
        next_record = MPost.get_next_record(current_id)
        if next_record is None:

            return self.render_string('modules/post/newest_page.html')
        else:
            kwd = {
                'uid': next_record.uid,
            }
            return self.render_string('modules/post/next_page.html', kwd=kwd)


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

    def render(self, uid_with_str):
        return self.render_string('modules/post/catalog_of.html',
                                  recs=MCategory.query_uid_starts_with(uid_with_str))


class PostCategoryOf(tornado.web.UIModule):
    '''
    The catalog of the post.
    '''

    def render(self, uid_with_str, slug=False, order=False):
        curinfo = MCategory.get_by_uid(uid_with_str)
        sub_cats = MCategory.query_sub_cat(uid_with_str)

        if slug:
            return self.render_string('modules/post/post_catalog_slug.html',
                                      pcatinfo=curinfo,
                                      sub_cats=sub_cats,
                                      recs=sub_cats,
                                      order=order)
        else:
            return self.render_string('modules/info/catalog_of.html',
                                      pcatinfo=curinfo,
                                      sub_cats=sub_cats,
                                      recs=sub_cats)


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
                                  unescape=tornado.escape.xhtml_unescape,
                                  kwd=kwd)


class LinkList(tornado.web.UIModule):
    '''
    return the list of links.
    '''

    def render(self, num=10):
        return self.render_string('modules/post/link_list.html',
                                  recs=MLink.query_link(num))


class PostCategoryRecent(tornado.web.UIModule):
    '''
    The reccent posts of certain category.
    '''

    def render(self, cat_id, label=None, num=10, with_catalog=True, with_date=True, glyph=''):

        catinfo = MCategory.get_by_uid(cat_id)
        if catinfo.pid == '0000':
            subcats = MCategory.query_sub_cat(cat_id)
            sub_cat_ids = [x.uid for x in subcats]
            recs = MPost.query_total_cat_recent(sub_cat_ids, label=label, num=num, kind=catinfo.kind)

        else:
            recs = MPost.query_cat_recent(cat_id, label=label, num=num, kind=catinfo.kind)

        kwd = {
            'with_catalog': with_catalog,
            'with_category': with_catalog,
            'with_date': with_date,
            'router': config.router_post[catinfo.kind],
            'glyph': glyph,
        }
        return self.render_string('modules/post/post_list.html',
                                  recs=recs,
                                  unescape=tornado.escape.xhtml_unescape,
                                  kwd=kwd)


class ShowoutRecent(tornado.web.UIModule):
    '''
    return posts of recent for showing out.
    '''

    def render(self, cat_id, kind, **kwargs):

        if 'num' in kwargs:
            num = kwargs['num']
        else:
            num = 10

        if 'width' in kwargs:
            width = kwargs['width']
        else:
            width = 160

        if 'height' in kwargs:
            height = kwargs['height']
        else:
            height = 120

        if 'with_catalog' in kwargs:
            with_catalog = kwargs['with_catalog']
        else:
            with_catalog = True

        if 'with_date' in kwargs:
            with_date = kwargs['with_date']
        else:
            with_date = True

        kwd = {
            'with_catalog': with_catalog,
            'with_date': with_date,
            'width': width,
            'height': height,
        }

        return self.render_string('modules/post/showout_list.html',
                                  recs=MPost.query_cat_recent(cat_id, num=num, kind=kind),
                                  unescape=tornado.escape.xhtml_unescape,
                                  kwd=kwd)


class SiteUrl(tornado.web.UIModule):
    '''
    return the url of the site.
    '''

    def render(self):
        return config.SITE_CFG['site_url']


class SiteTitle(tornado.web.UIModule):
    '''
    return the title of the site.
    '''

    def render(self):
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
                      MPost2Catalog().query_by_entity_uid(post_id).naive()]
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

    def render(self, html_str):
        tmp_str = bs4.BeautifulSoup(tornado.escape.xhtml_unescape(html_str), "html.parser")
        return tmp_str.get_text()[:130] + '....'


# Todo: should be deleted.
class GenerateDescription(tornado.web.UIModule):
    '''
    Just as GenerateAbstract
    '''

    def render(self, html_str):
        tmp_str = bs4.BeautifulSoup(tornado.escape.xhtml_unescape(html_str), "html.parser")
        return tmp_str.get_text()[:100]


class CategoryMenu(tornado.web.UIModule):
    '''
    Menu for category lists.
    '''

    def render(self, kind='1'):
        return self.render_string('modules/post/showcat_list.html',
                                  recs=MCategory.query_all(kind=kind),
                                  unescape=tornado.escape.xhtml_unescape)


class CopyRight(tornado.web.UIModule):
    '''
    show TorCMS copy right.
    '''

    def render(self):
        return '''<span>Build on
        <a href="https://github.com/bukun/TorCMS" target="_blank">TorCMS</a>.</span>'''


class PostTags(tornado.web.UIModule):
    '''
    show tags of the post.
    '''

    def render(self, uid, kind):
        out_str = ''
        ii = 1
        for tag_info in MPost2Catalog.query_by_entity_uid(uid, kind=kind).naive():
            tmp_str = '<a href="/category/{0}" class="tag{1}">{2}</a>'.format(
                tag_info.tag_slug,
                ii,
                tag_info.tag_name)
            out_str += tmp_str
            ii += 1
        return out_str


class MapTags(tornado.web.UIModule):
    '''
    show tags of the map.
    '''

    def render(self, uid):
        out_str = ''
        ii = 1
        for tag_info in MPost2Catalog.query_by_entity_uid(uid, kind='m').naive():
            tmp_str = '<a href="/tag/{0}" class="tag{1}">{2}</a>'.format(
                tag_info.tag_slug,
                ii,
                tag_info.tag_name)
            out_str += tmp_str
            ii += 1
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

    def render(self):
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

        cat_rec = MCategory.get_by_slug(cat_slug)
        num_of_cat = MPost2Catalog.count_of_certain_category(cat_rec.uid)

        pager_cnt = int(num_of_cat / config.CMS_CFG['list_num'])

        page_num = (pager_cnt if abs(pager_cnt - num_of_cat / config.CMS_CFG['list_num']) < 0.1
                    else pager_cnt + 1)

        kwd = {
            'page_home': False if current <= 1 else True,
            'page_end': False if current >= page_num else True,
            'page_pre': False if current <= 1 else True,
            'page_next': False if current >= page_num else True,
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

        page_num = int(cat_rec.count() / config.CMS_CFG['list_num'])

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

    def render(self, kind, *args, **kwargs):
        tag_slug = args[0]
        current = int(args[1])

        page_num = int(MPost2Label.total_number(tag_slug, kind) / config.CMS_CFG['list_num'])

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
        page_num = math_ceil(num_of_tag / config.CMS_CFG['list_num'])

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

    def render(self, *args):
        ysearch = YunSearch()
        catid = args[0]
        tag_slug = args[1]
        current = int(args[2])
        res_all = ysearch.get_all_num(tag_slug, catid=catid)
        page_num = int(res_all / config.CMS_CFG['list_num'])

        kwd = {
            'page_home': False if current <= 1 else True,
            'page_end': False if current >= page_num else True,
            'page_pre': False if current <= 1 else True,
            'page_next': False if current >= page_num else True,
        }

        return self.render_string('modules/post/search_pager.html',
                                  kwd=kwd,
                                  cat_slug=tag_slug,
                                  pager_num=page_num,
                                  page_current=current)


class AppTitle(tornado.web.UIModule):
    '''
    search widget. Simple searching. searching for all.
    '''

    def render(self, uid):
        rec = MPost.get_by_uid(uid=uid)
        return rec.title if rec else None
