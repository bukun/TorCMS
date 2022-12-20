# -*- coding:utf-8 -*-

from torcms.handlers.admin_handler import AdminHandler
from torcms.handlers.catalog_hander import CatalogHandler
from torcms.handlers.category_handler import CategoryAjaxHandler
from torcms.handlers.classify_hander import ClassifyHandler
from torcms.handlers.collect_handler import CollectHandler
from torcms.handlers.comment_hander import CommentHandler
from torcms.handlers.entity2user_handler import Entity2UserHandler
from torcms.handlers.entity_handler import EntityAjaxHandler, EntityHandler
from torcms.handlers.evaluation_handler import EvaluationHandler
from torcms.handlers.filter_handler import FilterHandler
from torcms.handlers.index import IndexHandler
from torcms.handlers.label_handler import InfoTagHandler, LabelHandler
from torcms.handlers.leaf_handler import LeafHandler
from torcms.handlers.link_handler import LinkHandler, LinkPartialHandler
from torcms.handlers.list_handler import ListHandler, TagListHandler
from torcms.handlers.log_handler import LogHandler, LogPartialHandler
from torcms.handlers.nullify_info_handler import NullifyInfoHandler
from torcms.handlers.page_ajax_handler import PageAjaxHandler
from torcms.handlers.page_handler import PageHandler
from torcms.handlers.post_ajax_handler import PostAjaxHandler
from torcms.handlers.post_handler import PostHandler
from torcms.handlers.post_history_handler import PostHistoryHandler
from torcms.handlers.post_list_handler import PostListHandler
from torcms.handlers.publish_handler import PublishHandler
from torcms.handlers.rating_handler import RatingHandler
from torcms.handlers.relation_handler import RelHandler
from torcms.handlers.reply_handler import ReplyHandler,ReplyAjaxHandler
from torcms.handlers.search_handler import SearchHandler
from torcms.handlers.sys_handler import SysHandler
from torcms.handlers.user_handler import UserHandler, UserPartialHandler
from torcms.handlers.user_info_list_handler import UserListHandler
from torcms.handlers.wiki_handler import WikiHandler
from torcms.handlers.wiki_history_manager import WikiHistoryHandler
from torcms.handlers.check_handler import CheckHandler

urls = [
    ('/_rating/(.*)', RatingHandler, {}),
    ('/post_man/(.*)', PostHistoryHandler, {}),
    ('/meta_man/(.*)', PostHistoryHandler, {}),
    ('/wiki_man/(.*)', WikiHistoryHandler, {}),
    ('/page_man/(.*)', WikiHistoryHandler, {}),
    ("/admin/(.*)", AdminHandler, {}),
    ("/entry/(.*)", EntityHandler, {}),
    ("/entity/(.*)", EntityHandler, {}),
    ("/entity_j/(.*)", EntityAjaxHandler, {}),
    ("/entity_download/(.*)", Entity2UserHandler, {}),

    # For listing items.
    ("/list/(.*)", ListHandler, {}),
    ("/post/(.*)", PostHandler, dict(kind='1')),

    # For listing ordered items.
    ("/catalog/(.*)", CatalogHandler, {}),
    ("/leaf/(.*)", LeafHandler, dict(kind='6')),

    # For filter listing.
    ("/filter/(.*)", FilterHandler, {}),

    # CRUD, for information via filter.
    ("/info/(.*)", PostHandler, dict(kind='3', filter_view=True)),
    ("/label/(.*)", LabelHandler, {}),
    ("/user/(.*)", UserHandler, {}),
    ("/user_j/(.*)", UserPartialHandler, {}),
    ("/post_j/(.*)", PostAjaxHandler, {}),
    ("/post_list/(.*)", PostListHandler, {}),
    ("/category_j/(.*)", CategoryAjaxHandler, {}),
    ("/link_j/(.*)", LinkPartialHandler, {}),
    ("/link/(.*)", LinkHandler, {}),
    ("/page_j/(.*)", PageAjaxHandler, {}),
    ("/page/(.*)", PageHandler, {}),
    ("/wiki/(.*)", WikiHandler, {}),
    ("/search/(.*)", SearchHandler, {}),
    ("/reply/(.*)", ReplyHandler, {}),
    ("/reply_j/(.*)", ReplyAjaxHandler, {}),
    ("/publish/(.*)", PublishHandler, {}),
    ("/collect/(.*)", CollectHandler, {}),
    ('/rel/(.*)', RelHandler, {}),
    ("/user_list/(.*)", UserListHandler, {}),
    ("/evaluate/(.*)", EvaluationHandler, {}),
    ("/sys/(.*)", SysHandler, {}),
    ("/log/(.*)", LogHandler, {}),
    ("/log_j/(.*)", LogPartialHandler, {}),
    ('/nullify_info/(.*)', NullifyInfoHandler, {}),
    ('/comment/(.*)', CommentHandler, {}),
    ('/classify/(.*)', ClassifyHandler, {}),
    ("/check/(.*)", CheckHandler, dict()),
    ("/", IndexHandler, {})
]
