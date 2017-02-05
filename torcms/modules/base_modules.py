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
from torcms.model.info_model import MInfor
from torcms.model.label_model import MPost2Label
from torcms.model.wiki_model import MWiki
from torcms.core.tool.whoosh_tool import YunSearch
from torcms.core.tools import logger
import config


class show_page(tornado.web.UIModule):
    '''

    '''
    def render(self, *args, **kwargs):
        '''
        '''
        page_id = kwargs['page_id']
        userinfo = kwargs['userinfo'] if 'userinfo' in kwargs else None
        page = MWiki.get_by_uid(page_id)
        kwd = {
            'uid': page_id,
        }
        if page:
            return self.render_string('modules/show_page.html',
                                      unescape=tornado.escape.xhtml_unescape,
                                      postinfo=page,
                                      userinfo=userinfo,
                                      kwd=kwd)
        else:
            return '<a href="/page/{0}">{0}</a>'.format(page_id)


class get_footer(tornado.web.UIModule):
    '''

    '''
    def render(self):
        logger.info('Init footer')
        all_cats = MCategory.query_all()
        kwd = {
            'cats': all_cats,
        }
        return self.render_string('modules/post/menu.html',
                                  kwd=kwd)


class previous_post_link(tornado.web.UIModule):
    '''

    '''
    def render(self, current_id):
        prev_record = MPost.get_previous_record(current_id)
        if prev_record is None:
            outstr = '<a>The last post.</a>'
        else:
            outstr = '''<a href="/post/{0}">Previous Post</a>'''.format(
                prev_record.uid
            )
        return outstr


class post_most_view(tornado.web.UIModule):
    '''

    '''
    def render(self, num, with_date=True, with_catalog=True):
        kwd = {
            'with_date': with_date,
            'with_catalog': with_catalog,
            'router': config.router_post['1'],
        }
        return self.render_string('modules/post/post_list.html',
                                  recs=MPost.query_most(num),
                                  kwd=kwd)


class post_random(tornado.web.UIModule):
    '''

    '''
    def render(self, num, with_date=True, with_catalog=True):
        kwd = {
            'with_date': with_date,
            'with_catalog': with_catalog,
            'router': config.router_post['1']
        }
        return self.render_string('modules/post/post_list.html',
                                  recs=MPost.query_random(num),
                                  kwd=kwd)


class post_cat_random(tornado.web.UIModule):
    '''

    '''
    def render(self, cat_id, num, with_date=True, with_catalog=True):
        kwd = {
            'with_date': with_date,
            'with_catalog': with_catalog,
            'router': config.router_post['1'],
        }
        return self.render_string('modules/post/post_list.html',
                                  recs=MPost.query_cat_random(cat_id, num),
                                  kwd=kwd)


class post_recent_most_view(tornado.web.UIModule):
    '''

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


class catalog_of(tornado.web.UIModule):
    '''

    '''
    def render(self, uid_with_str):
        return self.render_string('modules/post/catalog_of.html',
                                  recs=MCategory.query_uid_starts_with(uid_with_str))


class post_catalog_of(tornado.web.UIModule):
    '''

    '''
    def render(self, uid_with_str, slug=False):
        curinfo = MCategory.get_by_uid(uid_with_str)
        sub_cats = MCategory.query_sub_cat(uid_with_str)

        if slug:
            return self.render_string('modules/post/post_catalog_slug.html',
                                      pcatinfo=curinfo,
                                      sub_cats=sub_cats,
                                      recs=sub_cats)
        else:
            return self.render_string('modules/info/catalog_of.html',
                                      pcatinfo=curinfo,
                                      sub_cats=sub_cats,
                                      recs=sub_cats)


class post_recent(tornado.web.UIModule):
    '''

    '''
    def render(self, num=10, with_catalog=True, with_date=True):
        kwd = {
            'with_date': with_date,
            'with_catalog': with_catalog,
            'router': config.router_post['1'],
        }
        return self.render_string('modules/post/post_list.html',
                                  recs=MPost.query_recent(num),
                                  unescape=tornado.escape.xhtml_unescape,
                                  kwd=kwd)


class link_list(tornado.web.UIModule):
    '''

    '''
    def render(self, num=10):
        return self.render_string('modules/post/link_list.html',
                                  recs=MLink.query_link(num))


class post_category_recent(tornado.web.UIModule):
    '''

    '''
    def render(self, cat_id, num=10, with_catalog=True, with_date=True):
        catinfo = MCategory.get_by_uid(cat_id)
        recs = MPost.query_cat_recent(cat_id, num, kind=catinfo.kind)
        kwd = {
            'with_catalog': with_catalog,
            'with_date': with_date,
            'router': config.router_post[catinfo.kind],
        }
        return self.render_string('modules/post/post_list.html',
                                  recs=recs,
                                  unescape=tornado.escape.xhtml_unescape,
                                  kwd=kwd)


class showout_recent(tornado.web.UIModule):
    '''

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
                                  recs=MPost.query_cat_recent(cat_id, num, kind),
                                  unescape=tornado.escape.xhtml_unescape,
                                  kwd=kwd)


class site_url(tornado.web.UIModule):
    '''

    '''
    def render(self):
        return config.SITE_CFG['site_url']


class site_title(tornado.web.UIModule):
    '''

    '''
    def render(self):
        return ''


class next_post_link(tornado.web.UIModule):
    '''

    '''
    def render(self, current_id):
        next_record = MPost.get_next_record(current_id)
        if next_record is None:
            outstr = '<a>The newest post.</a>'
        else:
            outstr = '''<a href="/post/{0}">Next Post</a>'''.format(next_record.uid)
        return outstr


class the_category(tornado.web.UIModule):
    '''

    '''
    def render(self, post_id):
        tmpl_str = '''<a href="/category/{0}">{1}</a>'''
        format_arr = [tmpl_str.format(uu.tag.slug, uu.tag.name) for uu in
                      MPost2Catalog().query_by_entity_uid(post_id)]
        return ', '.join(format_arr)


class list_categories(tornado.web.UIModule):
    '''

    '''
    def render(self, cat_id, list_num):
        recs = MPost.query_cat_recent(cat_id, list_num)
        out_str = ''
        for rec in recs:
            tmp_str = '''<li><a href="/{0}">{1}</a></li>'''.format(
                rec.title,
                rec.title
            )
            out_str += tmp_str
        return out_str


class generate_abstract(tornado.web.UIModule):
    '''

    '''
    def render(self, html_str):
        tmp_str = bs4.BeautifulSoup(tornado.escape.xhtml_unescape(html_str), "html.parser")
        return tmp_str.get_text()[:130] + '....'


class generate_description(tornado.web.UIModule):
    '''

    '''
    def render(self, html_str):
        tmp_str = bs4.BeautifulSoup(tornado.escape.xhtml_unescape(html_str), "html.parser")
        return tmp_str.get_text()[:100]


class category_menu(tornado.web.UIModule):
    '''

    '''
    def render(self):
        return self.render_string('modules/post/showcat_list.html',
                                  recs=MCategory.query_all(),
                                  unescape=tornado.escape.xhtml_unescape)


class copyright(tornado.web.UIModule):
    '''

    '''
    def render(self):
        return '''<span>Build on
        <a href="https://github.com/bukun/TorCMS" target="_blank">TorCMS</a>.</span>'''


class post_tags(tornado.web.UIModule):
    '''

    '''
    def render(self, signature):
        out_str = ''
        ii = 1
        for tag_info in MPost2Catalog.query_by_entity_uid(signature, kind='1'):
            tmp_str = '<a href="/category/{0}" class="tag{1}">{2}</a>'.format(
                tag_info.tag.slug,
                ii,
                tag_info.tag.name)
            out_str += tmp_str
            ii += 1
        return out_str


class map_tags(tornado.web.UIModule):
    '''

    '''
    def render(self, signature):
        out_str = ''
        ii = 1
        for tag_info in MPost2Catalog.query_by_entity_uid(signature, kind='m'):
            tmp_str = '<a href="/tag/{0}" class="tag{1}">{2}</a>'.format(
                tag_info.tag.slug,
                ii,
                tag_info.tag.name)
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
        return self.render_string('modules/post/topline.html')


class catalog_pager(tornado.web.UIModule):
    '''

    '''
    def render(self, *args, **kwargs):
        cat_slug = args[0]
        current = int(args[1])
        # cat_slug 分类
        # current 当前页面

        cat_rec = MCategory.get_by_slug(cat_slug)
        num_of_cat = MPost2Catalog.count_of_certain_category(cat_rec.uid)

        tmp_page_num = int(num_of_cat / config.CMS_CFG['list_num'])

        page_num = (tmp_page_num if abs(tmp_page_num - num_of_cat / config.CMS_CFG['list_num']) < 0.1
                    else tmp_page_num + 1)

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


class info_label_pager(tornado.web.UIModule):
    '''

    '''
    def render(self, *args, **kwargs):
        tag_slug = args[0]
        current = int(args[1])

        cat_rec = MInfor.query_by_tagname(tag_slug)

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


class label_pager(tornado.web.UIModule):
    '''

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


class tag_pager(tornado.web.UIModule):
    '''

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


class search_pager(tornado.web.UIModule):
    '''

    '''
    def render(self, *args, **kwargs):
        ysearch = YunSearch()
        tag_slug = args[0]
        current = int(args[1])
        res_all = ysearch.get_all_num(tag_slug)
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
