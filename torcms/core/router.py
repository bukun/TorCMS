# -*- coding:utf-8 -*-

from torcms.handlers.admin_handler import AdminHandler
from torcms.handlers.catalog_handler import CatalogHandler
from torcms.handlers.category_handler import CategoryHandler, TagListHandler
from torcms.handlers.collect_handler import CollectHandler
from torcms.handlers.entity_handler import EntityHandler
from torcms.handlers.evaluation_handler import EvaluationHandler
from torcms.handlers.filter_handler import FilterHandler
from torcms.handlers.index import IndexHandler
from torcms.handlers.label_handler import LabelHandler, InfoTagHandler
from torcms.handlers.leaf_handler import LeafHandler
from torcms.handlers.link_handler import LinkHandler, LinkPartialHandler
from torcms.handlers.maintain_handler import MaintainCategoryHandler, MaintainCategoryAjaxHandler
from torcms.handlers.maintain_info_handler import MaintainPycateCategoryHandler
from torcms.handlers.page_ajax_handler import PageAjaxHandler
from torcms.handlers.page_handler import PageHandler
from torcms.handlers.post_ajax_handler import PostAjaxHandler
from torcms.handlers.post_handler import PostHandler
from torcms.handlers.post_history_handler import PostHistoryHandler
from torcms.handlers.post_list_handler import PostListHandler
from torcms.handlers.publish_handler import PublishHandler
from torcms.handlers.rating_handler import RatingHandler
from torcms.handlers.relation_handler import RelHandler
from torcms.handlers.reply_handler import ReplyHandler
from torcms.handlers.search_handler import SearchHandler
from torcms.handlers.user_handler import UserHandler, UserPartialHandler
from torcms.handlers.user_info_list_handler import UserListHandler
from torcms.handlers.wiki_handler import WikiHandler
from torcms.handlers.wiki_history_manager import WikiHistoryHandler


urls = [

    ('/_rating/(.*)', RatingHandler, dict()),

    ('/post_man/(.*)', PostHistoryHandler, dict()),
    ('/meta_man/(.*)', PostHistoryHandler, dict()),
    ('/wiki_man/(.*)', WikiHistoryHandler, dict()),
    ('/page_man/(.*)', WikiHistoryHandler, dict()),

    ("/admin/(.*)", AdminHandler, dict()),
    ("/entry/(.*)", EntityHandler, dict()),
    ("/entity/(.*)", EntityHandler, dict()),

    ("/label/(.*)", LabelHandler, dict()),
    ("/catalog/(.*)", CatalogHandler, dict()),
    ("/category/(.*)", CategoryHandler, dict()),

    ("/tag/(.*)", TagListHandler, dict()),  # Deprecated, replaed by `/category` .

    ("/user/p/(.*)", UserPartialHandler, dict()),  # Deprecated
    ("/user_p/(.*)", UserPartialHandler, dict()),  # Deprecated
    ("/user_j/(.*)", UserPartialHandler, dict()),
    ("/user/(.*)", UserHandler, dict()),
    ("/post_j/(.*)", PostAjaxHandler, dict()),
    ("/post_p/(.*)", PostAjaxHandler, dict()),  # Deprecated,
    ("/post/p/(.*)", PostAjaxHandler, dict()),  # Deprecated,
    # ("/post/(.*)", PostHandler, dict()),

    ("/post/(.*)", PostHandler, dict(kind='1')),
    ("/leaf/(.*)", LeafHandler, dict(kind='1')),

    ("/post_list/(.*)", PostListHandler, dict()),

    ("/maintain/p/category/(.*)", MaintainCategoryAjaxHandler, dict()),
    ("/maintain/category/(.*)", MaintainCategoryHandler, dict()),
    ("/link/p/(.*)", LinkPartialHandler, dict()),  # deprecated
    ("/link_j/(.*)", LinkHandler, dict()),
    ("/link/(.*)", LinkHandler, dict()),

    ("/page/p/(.*)", PageAjaxHandler, dict()),  # Deprecated
    ("/page_p/(.*)", PageAjaxHandler, dict()),  # Deprecated
    ("/page_j/(.*)", PageAjaxHandler, dict()),
    ("/page/(.*)", PageHandler, dict()),
    ("/wiki/(.*)", WikiHandler, dict()),
    ("/search/(.*)", SearchHandler, dict()),
    ("/reply/(.*)", ReplyHandler, dict()),

    ("/info/(.*)", PostHandler, dict(kind='9', filter_view=True)),

    ("/maintain/claslitecategory/(.*)", MaintainPycateCategoryHandler, dict()),

    ("/filter/(.*)", FilterHandler, dict()),
    ("/list/(.*)", FilterHandler, dict()),  # Deprecated, replaed by `/filter` .

    ("/publish/(.*)", PublishHandler, dict()),

    # Todo: need to be deleted. replaced by `/label/`.
    ('/info_tag/(.*)', InfoTagHandler, dict()),

    ("/collect/(.*)", CollectHandler, dict()),
    ('/rel/(.*)', RelHandler, dict()),
    ("/user_list/(.*)", UserListHandler, dict()),

    ("/evaluate/(.*)", EvaluationHandler, dict()),
    ("/", IndexHandler, dict()),

]
