# -*- coding:utf-8 -*-
from  math import ceil as math_ceil
import bs4
import tornado.escape
import tornado.web
from torcms.model.post_model import MPost
from torcms.model.link_model import MLink
from torcms.model.post2catalog_model import MPost2Catalog
import tornado.web
from torcms.model.category_model import MCategory
from torcms.model.info_model import MInfor as  MInfor
from torcms.model.label_model import MPost2Label
from torcms.model.reply_model import MReply
from torcms.model.page_model import MPage
from torcms.model.infor2catalog_model import MInfor2Catalog
from torcms.core.tool.whoosh_tool import yunsearch
import config
from config import router_post

mreply = MReply()
mpage = MPage()


class show_page(tornado.web.UIModule):
    def render(self, page_id):
        page = mpage.get_by_uid(page_id)
        if page:
            return self.render_string('modules/show_page.html',
                                      unescape=tornado.escape.xhtml_unescape,
                                      postinfo=page
                                      )
        else:
            return '<a href="/page/{0}">{0}</a>'.format(page_id)


class get_footer(tornado.web.UIModule):
    def render(self):
        self.mcat = MCategory()
        all_cats = self.mcat.query_all()
        kwd = {
            'cats': all_cats,
        }
        return self.render_string('modules/post/menu.html',
                                  kwd=kwd)


class previous_post_link(tornado.web.UIModule):
    def render(self, current_id):
        self.mpost = MPost()
        prev_record = self.mpost.get_previous_record(current_id)
        if prev_record is None:
            outstr = '<a>The last post.</a>'
        else:
            outstr = '''<a href="/post/{0}">Previous Post</a>'''.format(prev_record.uid, prev_record.title)
        return outstr


class post_most_view(tornado.web.UIModule):
    def render(self, num, with_date=True, with_catalog=True):
        self.mpost = MPost()
        recs = self.mpost.query_most(num)
        kwd = {
            'with_date': with_date,
            'with_catalog': with_catalog,
            'router': router_post['1'],
        }
        return self.render_string('modules/post/post_list.html', recs=recs, kwd=kwd)


class post_random(tornado.web.UIModule):
    def render(self, num, with_date=True, with_catalog=True):
        self.mpost = MPost()
        recs = self.mpost.query_random(num)
        kwd = {
            'with_date': with_date,
            'with_catalog': with_catalog,
            'router': router_post['1'],
        }
        return self.render_string('modules/post/post_list.html',
                                  recs=recs, kwd=kwd)


class post_cat_random(tornado.web.UIModule):
    def render(self, cat_id, num, with_date=True, with_catalog=True):
        self.mpost = MPost()
        recs = self.mpost.query_cat_random(cat_id, num)
        kwd = {
            'with_date': with_date,
            'with_catalog': with_catalog,
            'router': router_post['1'],
        }
        return self.render_string('modules/post/post_list.html',
                                  recs=recs, kwd=kwd)


class post_recent_most_view(tornado.web.UIModule):
    def render(self, num, recent, with_date=True, with_catalog=True):
        self.mpost = MPost()
        recs = self.mpost.query_recent_most(num, recent)
        kwd = {
            'with_date': with_date,
            'with_catalog': with_catalog,
            'router': router_post['1'],
        }
        return self.render_string('modules/post/post_list.html', recs=recs, kwd=kwd)


class catalog_of(tornado.web.UIModule):
    def render(self, uid_with_str):
        self.mcat = MCategory()
        recs = self.mcat.query_uid_starts_with(uid_with_str)

        return self.render_string('modules/post/catalog_of.html',
                                  recs=recs)


class post_recent(tornado.web.UIModule):
    def render(self, num=10, with_catalog=True, with_date=True):
        self.mpost = MPost()
        recs = self.mpost.query_recent(num)
        kwd = {
            'with_date': with_date,
            'with_catalog': with_catalog,
            'router': router_post['1'],
        }
        return self.render_string('modules/post/post_list.html',
                                  recs=recs,
                                  unescape=tornado.escape.xhtml_unescape,
                                  kwd=kwd, )


class link_list(tornado.web.UIModule):
    def render(self, num=10):
        self.mlink = MLink()
        recs = self.mlink.query_link(num)
        return self.render_string('modules/post/link_list.html',
                                  recs=recs,
                                  )


class post_category_recent(tornado.web.UIModule):
    def render(self, cat_id, num=10, with_catalog=True, with_date=True):
        self.mcat = MCategory()
        self.mpost = MPost()
        self.mpost2cat = MPost2Catalog()
        catinfo = self.mcat.get_by_uid(cat_id)
        recs = self.mpost.query_cat_recent(cat_id, num, kind = catinfo.kind)
        kwd = {
            'with_catalog': with_catalog,
            'with_date': with_date,
            'router': router_post[catinfo.kind],
        }
        return self.render_string('modules/post/post_list.html',
                                  recs=recs,
                                  unescape=tornado.escape.xhtml_unescape,
                                  kwd=kwd, )


class showout_recent(tornado.web.UIModule):
    def render(self, cat_id, kind,num=10, with_catalog=True, with_date=True, width=160, height=120):
        self.mpost = MPost()
        self.mpost2cat = MPost2Catalog()
        recs = self.mpost.query_cat_recent(cat_id, num,kind)

        kwd = {
            'with_catalog': with_catalog,
            'with_date': with_date,
            'width': width,
            'height': height,
        }

        return self.render_string('modules/post/showout_list.html',
                                  recs=recs,
                                  unescape=tornado.escape.xhtml_unescape,
                                  kwd=kwd, )


class site_url(tornado.web.UIModule):
    def render(self):
        return config.site_url

class site_title(tornado.web.UIModule):
    def render(self):
        return config.site_title

class next_post_link(tornado.web.UIModule):
    def render(self, current_id):
        self.mpost = MPost()
        next_record = self.mpost.get_next_record(current_id)
        if next_record is None:
            outstr = '<a>The newest post.</a>'
        else:
            outstr = '''<a href="/post/{0}">Next Post</a>'''.format(next_record.uid)
        return outstr


class the_category(tornado.web.UIModule):
    def render(self, post_id):
        tmpl_str = '''<a href="/category/{0}">{1}</a>'''
        format_arr = [tmpl_str.format(uu.tag.slug, uu.tag.name) for uu in
                      MPost2Catalog().query_by_entity_uid(post_id)]
        return ', '.join(format_arr)


class list_categories(tornado.web.UIModule):
    def render(self, cat_id, list_num):
        self.mpost = MPost()
        recs = self.mpost.query_by_cat(cat_id, list_num)
        out_str = ''
        for rec in recs:
            tmp_str = '''<li><a href="/{0}">{1}</a></li>'''.format(rec.title, rec.title)
            out_str += tmp_str
        return out_str


class generate_abstract(tornado.web.UIModule):
    def render(self, html_str):
        tmp_str = bs4.BeautifulSoup(tornado.escape.xhtml_unescape(html_str), "html.parser")
        return tmp_str.get_text()[:130] + '....'


class generate_description(tornado.web.UIModule):
    def render(self, html_str):
        tmp_str = bs4.BeautifulSoup(tornado.escape.xhtml_unescape(html_str), "html.parser")
        return tmp_str.get_text()[:100]


class category_menu(tornado.web.UIModule):
    def render(self):
        self.mcat = MCategory()
        recs = self.mcat.query_all()
        return self.render_string('modules/post/showcat_list.html',
                                  recs=recs,
                                  unescape=tornado.escape.xhtml_unescape,
                                  )


class copyright(tornado.web.UIModule):
    def render(self):
        out_str = '''<span>Build on <a href="https://github.com/bukun/TorCMS" target="_blank">TorCMS</a>.</span>'''
        return (out_str)


class post_tags(tornado.web.UIModule):
    def render(self, signature):
        self.mapp2tag = MPost2Catalog()
        tag_infos = self.mapp2tag.query_by_entity_uid(signature, kind='1')
        out_str = ''
        ii = 1
        for tag_info in tag_infos:
            tmp_str = '<a href="/category/{0}" class="tag{1}">{2}</a>'.format(tag_info.tag.slug, ii,
                                                                              tag_info.tag.name)
            out_str += tmp_str
            ii += 1
        return out_str
class map_tags(tornado.web.UIModule):
    def render(self, signature):
        self.mapp2tag = MPost2Catalog()
        tag_infos = self.mapp2tag.query_by_entity_uid(signature, kind='m')
        out_str = ''
        ii = 1
        for tag_info in tag_infos:
            tmp_str = '<a href="/tag/{0}" class="tag{1}">{2}</a>'.format(tag_info.tag.slug, ii,
                                                                              tag_info.tag.name)
            out_str += tmp_str
            ii += 1
        return out_str


class ModuleCatMenu(tornado.web.UIModule):
    def render(self, with_count=True):
        self.mcat = MCategory()
        all_cats = self.mcat.query_all(by_count=True)
        kwd = {
            'cats': all_cats,
            'with_count': with_count,
        }
        return self.render_string('modules/post/menu_post.html',
                                  kwd=kwd)


class ToplineModule(tornado.web.UIModule):
    def render(self):
        return self.render_string('modules/post/topline.html')





class catalog_pager(tornado.web.UIModule):
    def render(self, *args, **kwargs):
        self.mpost2catalog = MPost2Catalog()
        self.mcat = MCategory()

        cat_slug = args[0]
        current = int(args[1])
        # cat_slug 分类
        # current 当前页面

        cat_rec = self.mcat.get_by_slug(cat_slug)
        num_of_cat = self.mpost2catalog.count_of_certain_category(cat_rec.uid)

        tmp_page_num = int(num_of_cat / config.page_num)

        page_num = tmp_page_num if abs(tmp_page_num - num_of_cat / config.page_num) < 0.1 else  tmp_page_num + 1

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
                                  page_current=current,
                                  )


class info_label_pager(tornado.web.UIModule):
    def render(self, *args, **kwargs):
        self.minfo = MInfor()
        tag_slug = args[0]
        current = int(args[1])

        cat_rec = self.minfo.query_by_tagname(tag_slug)

        page_num = int(cat_rec.count() / config.page_num)

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
                                  page_current=current,
                                  )


class label_pager(tornado.web.UIModule):
    def render(self,kind, *args, **kwargs):
        self.mapp2tag = MPost2Label()
        tag_slug = args[0]
        current = int(args[1])

        page_num = int(self.mapp2tag.total_number(tag_slug,kind) / config.page_num)

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
                                  kind = kind,
                                  )
class tag_pager(tornado.web.UIModule):
    def render(self, *args, **kwargs):
        self.mapp2tag = MInfor2Catalog()
        self.mcat = MCategory()
        tag_slug = args[0]
        current = int(args[1])
        taginfo = self.mcat.get_by_slug(tag_slug)
        num_of_tag = self.mapp2tag.count_of_certain_category(taginfo.uid)
        page_num = math_ceil(num_of_tag / config.page_num)

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
                                  page_current=current,
                                  )
class search_pager(tornado.web.UIModule):
    def render(self, *args, **kwargs):

        self.ysearch = yunsearch()
        tag_slug = args[0]
        current = int(args[1])
        res_all = self.ysearch.get_all_num(tag_slug)
        page_num = int(res_all / config.page_num)


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
                                  page_current=current,
                                  )
