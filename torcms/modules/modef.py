# -*- coding:utf-8 -*-

'''
define the Core Modules of TorCMS.
'''
from torcms.modules import base_modules
from torcms.modules import info_modules
from torcms.modules import widget_modules
from torcms.modules import catalog_modules
from torcms.modules import category_modules

core_modules = {
    'ModuleCatMenu': base_modules.ModuleCatMenu,
    'get_footer': base_modules.GetFooter,
    'previous_post_link': base_modules.PreviousPostLink,
    'next_post_link': base_modules.NextPostLink,
    'the_category': base_modules.TheCategory,
    'list_categories': base_modules.ListCategories,
    'post_most_view': base_modules.PostMostView,
    'post_random': base_modules.PostRandom,
    'post_recent': base_modules.PostRecent,
    'post_labels': base_modules.PostLabels,
    'link_list': base_modules.LinkList,
    'post_recent_most_view': base_modules.PostRecentMostView,
    'post_cat_random': base_modules.PostCatRandom,
    'post_cat_recent': base_modules.PostCategoryRecent,
    'showout_recent': base_modules.ShowoutRecent,
    'generate_abstract': base_modules.GenerateAbstract,
    'category_menu': category_modules.CategoryMenu,
    'site_url': base_modules.SiteUrl,
    'site_title': base_modules.SiteTitle,
    'generate_description': base_modules.GenerateDescription,
    'post_tags': base_modules.PostTags,
    'post_catalogs': base_modules.PostTags,
    'map_catalogs': base_modules.MapTags,
    'post_categories': base_modules.PostTags,
    'catalog_pager': base_modules.CategoryPager,
    'info_label_pager': base_modules.InfoLabelPager,
    'label_pager': base_modules.LabelPager,
    'tag_pager': base_modules.TagPager,
    'search_pager': base_modules.SearchPager,
    'collect_pager': base_modules.CollectPager,
    'catalog_of': base_modules.CategoryOf,
    'post_catalog_of': base_modules.PostCategoryOf,
    'show_page': base_modules.ShowPage,
    'Topline': base_modules.ToplineModule,
    'collect': base_modules.Collect,
    'user_collect': base_modules.UserCollect,

    'torcms_copyright': base_modules.CopyRight,
    'entity_list': base_modules.EntityList,
    'entity_pager': base_modules.EntityPager,
    'entity_download_user': base_modules.Entity2UserPager,
    'entity_download_list': base_modules.Entity2Pager,

    # widget
    'reply_panel': widget_modules.ReplyPanel,
    'baidu_share': widget_modules.BaiduShare,
    'widget_search': widget_modules.WidgetSearch,
    'widget_editor': widget_modules.WidgetEditor,
    'star_rating': widget_modules.StarRating,
    'use_f2e': widget_modules.UseF2E,
    'navigate_panel': widget_modules.NavigatePanel,
    'footer_panel': widget_modules.FooterPanel,
    'loginfo': widget_modules.UserinfoWidget,

    # Infor
    'app_catalog_of': info_modules.InfoCategory,
    'Banner': info_modules.BannerModule,
    'BreadCrumb': info_modules.BreadCrumb,
    'parentname': info_modules.ParentName,
    'catname': info_modules.CatName,
    'ContactInfo': info_modules.ContactInfo,
    'BreadcrumbPublish': info_modules.BreadcrumbPublish,
    'ImgSlide': info_modules.ImgSlide,
    'user_info': info_modules.UserInfo,
    'vip_info': info_modules.VipInfo,
    'rel_post2app': info_modules.RelPost2app,
    'rel_app2post': info_modules.RelApp2post,
    'app_random_choose': info_modules.InfoRandom,
    'app_tags': info_modules.InfoTags,
    'app_menu': info_modules.InfoMenu,
    'app_user_recent': info_modules.InfoUserRecent,
    'app_user_most': info_modules.InforUserMost,
    'app_recent_used': info_modules.InfoRecentUsed,
    'app_most_used': info_modules.InfoMostUsed,
    'label_count': info_modules.LabelCount,
    'baidu_search': widget_modules.BaiduSearch,
    'app_most_used_by_cat': info_modules.InfoMostUsedByCategory,
    'app_least_used_by_cat': info_modules.InfoLeastUseByCategory,
    'app_user_recent_by_cat': info_modules.InfoUserRecentByCategory,
    'app_title': base_modules.AppTitle,
    # 'entity_path_by_id': base_modules.Entity_path,
    'user_name_by_id': base_modules.UserName,
    'reply_post_by_id': base_modules.ReplyPostById,
    'category_by_slug': base_modules.CategoryBySlug,

    # # 'ext_category_menu': catalog_modules.CatalogMenu,
    'catalog_menu': catalog_modules.CatalogMenu,
    # # 'ext_category_list': catalog_modules.CatalogList,
    'catalog_list': catalog_modules.CatalogList,
    'postlistoftag': base_modules.PostListOfTag,
    'admin_post_pager':base_modules.Admin_Post_pager,
    'admin_page_pager':base_modules.Admin_Page_pager,
    'admin_reply_pager':base_modules.Admin_reply_pager

}
