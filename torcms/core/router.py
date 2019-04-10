# -*- coding:utf-8 -*-

from torcms.handlers.admin_handler import AdminHandler
from torcms.handlers.list_handler import ListHandler, TagListHandler
from torcms.handlers.collect_handler import CollectHandler
from torcms.handlers.entity_handler import EntityHandler, EntityAjaxHandler
from torcms.handlers.evaluation_handler import EvaluationHandler
from torcms.handlers.filter_handler import FilterHandler
from torcms.handlers.index import IndexHandler
from torcms.handlers.label_handler import LabelHandler, InfoTagHandler
from torcms.handlers.leaf_handler import LeafHandler
from torcms.handlers.link_handler import LinkHandler, LinkPartialHandler
from torcms.handlers.category_handler import CategoryAjaxHandler

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
from torcms.handlers.entity2user_handler import Entity2UserHandler
from torcms.handlers.catalog_hander import CatalogHandler
from torcms.handlers.sys_handler import SysHandler
from torcms.handlers.log_handler import LogHandler, LogPartialHandler

urls = [
    ('/_rating/(.*)', RatingHandler, dict()),

    ('/post_man/(.*)', PostHistoryHandler, dict()),
    ('/meta_man/(.*)', PostHistoryHandler, dict()),
    ('/wiki_man/(.*)', WikiHistoryHandler, dict()),
    ('/page_man/(.*)', WikiHistoryHandler, dict()),

    ("/admin/(.*)", AdminHandler, dict()),
    ("/entry/(.*)", EntityHandler, dict()),
    ("/entity/(.*)", EntityHandler, dict()),
    ("/entity_j/(.*)", EntityAjaxHandler, dict()),
    ("/entity_download/(.*)", Entity2UserHandler, dict()),

    # For listing items.

    # ToDo: To check.
    ("/list/(.*)", ListHandler, dict()),  # use to be category
    ("/post/(.*)", PostHandler, dict(kind='1')),

    # For listing ordered items.
    ("/catalog/(.*)", CatalogHandler, dict()),
    ("/leaf/(.*)", LeafHandler, dict(kind='6')),

    # For filter listing.
    ("/filter/(.*)", FilterHandler, dict()),
    ("/info/(.*)", PostHandler, dict(kind='9', filter_view=True)),

    ("/label/(.*)", LabelHandler, dict()),

    ("/user/(.*)", UserHandler, dict()),
    ("/user_j/(.*)", UserPartialHandler, dict()),

    ("/post_j/(.*)", PostAjaxHandler, dict()),

    ("/post_list/(.*)", PostListHandler, dict()),

    ("/category_j/(.*)", CategoryAjaxHandler, dict()),

    ("/link_j/(.*)", LinkPartialHandler, dict()),
    ("/link/(.*)", LinkHandler, dict()),

    ("/page_j/(.*)", PageAjaxHandler, dict()),
    ("/page/(.*)", PageHandler, dict()),
    ("/wiki/(.*)", WikiHandler, dict()),
    ("/search/(.*)", SearchHandler, dict()),
    ("/reply/(.*)", ReplyHandler, dict()),

    ("/publish/(.*)", PublishHandler, dict()),

    ("/collect/(.*)", CollectHandler, dict()),
    ('/rel/(.*)', RelHandler, dict()),
    ("/user_list/(.*)", UserListHandler, dict()),

    ("/evaluate/(.*)", EvaluationHandler, dict()),
    ("/sys/(.*)", SysHandler, dict()),
    ("/log/(.*)", LogHandler, dict()),
    ("/log_j/(.*)", LogPartialHandler, dict()),
    ("/", IndexHandler, dict())
]
