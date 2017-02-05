# -*- coding:utf-8 -*-

'''
define the Core Modules of TorCMS.
'''

from torcms.modules import base_modules
from torcms.modules import map_modules
from torcms.modules import widget_modules
from torcms.modules import info_modules

core_modules = {
    'ModuleCatMenu': base_modules.ModuleCatMenu,
    'get_footer': base_modules.get_footer,
    'previous_post_link': base_modules.previous_post_link,
    'next_post_link': base_modules.next_post_link,
    'the_category': base_modules.the_category,
    'list_categories': base_modules.list_categories,
    'post_most_view': base_modules.post_most_view,
    'post_random': base_modules.post_random,
    'post_recent': base_modules.post_recent,
    'link_list': base_modules.link_list,
    'post_recent_most_view': base_modules.post_recent_most_view,
    'post_cat_random': base_modules.post_cat_random,
    'post_cat_recent': base_modules.post_category_recent,
    'showout_recent': base_modules.showout_recent,
    'generate_abstract': base_modules.generate_abstract,
    'category_menu': base_modules.category_menu,
    'site_url': base_modules.site_url,
    'site_title': base_modules.site_title,
    'generate_description': base_modules.generate_description,
    'post_tags': base_modules.post_tags,
    'post_catalogs': base_modules.post_tags,
    'map_catalogs': base_modules.map_tags,
    'post_categories': base_modules.post_tags,
    'catalog_pager': base_modules.catalog_pager,
    'info_label_pager': base_modules.info_label_pager,
    'label_pager': base_modules.label_pager,
    'tag_pager': base_modules.tag_pager,
    'search_pager': base_modules.search_pager,
    'catalog_of': base_modules.catalog_of,
    'post_catalog_of': base_modules.post_catalog_of,
    'show_page': base_modules.show_page,
    'Topline': base_modules.ToplineModule,

    # 'copyright': copyright,

    # widget
    'reply_panel': widget_modules.reply_panel,
    'baidu_share': widget_modules.baidu_share,
    'widget_search': widget_modules.widget_search,
    'widget_editor': widget_modules.widget_editor,
    'star_rating': widget_modules.star_rating,
    'use_f2e': widget_modules.use_f2e,
    'navigate_panel': widget_modules.navigate_panel,
    'footer_panel': widget_modules.footer_panel,

    # Map
    'app_layout': map_modules.MapLayout,
    'app_json': map_modules.MapJson,

    # Infor
    'app_catalog_of': info_modules.InfoCategory,
    'Banner': info_modules.BannerModule,
    'BreadCrumb': info_modules.BreadCrumb,
    'parentname': info_modules.parentname,
    'catname': info_modules.catname,
    'ContactInfo': info_modules.ContactInfo,
    'BreadcrumbPublish': info_modules.BreadcrumbPublish,
    'ImgSlide': info_modules.ImgSlide,
    'user_info': info_modules.UserInfo,
    'vip_info': info_modules.VipInfo,
    'rel_post2app': info_modules.rel_post2app,
    'rel_app2post': info_modules.rel_app2post,
    'app_most_used': info_modules.InfoMostUsed,
    'app_random_choose': info_modules.app_random_choose,
    'app_tags': info_modules.app_tags,
    'app_menu': info_modules.app_menu,
    'app_user_recent': info_modules.InfoUserRecent,
    'app_user_most': info_modules.InforUserMost,
    'app_recent_used': info_modules.InfoRecentUsed,
    'label_count': info_modules.label_count,
    'baidu_search': info_modules.baidu_search,
    'app_most_used_by_cat': info_modules.app_most_used_by_cat,
    'app_least_used_by_cat': info_modules.app_least_use_by_cat,
    'app_user_recent_by_cat': info_modules.app_user_recent_by_cat,

}
