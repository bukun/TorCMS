# -*- coding:utf-8 -*-

from torcms.handlers.info_handler import InfoHandler
from torcms.handlers.info2_list_handler import InfoListHandler
from torcms.handlers.info2_publish_handler import InfoPublishHandler
from torcms.handlers.admin_handler import AdminHandler
from torcms.handlers.category_handler import CategoryHandler
from torcms.handlers.entity_handler import EntityHandler
from torcms.handlers.index import IndexHandler
from torcms.handlers.info_category_hanlder import InforCategoryHandler

from torcms.handlers.info2_tag_hanler import InfoTagHandler
from torcms.handlers.post_label_handler import PostLabelHandler
from torcms.handlers.link_handler import LinkHandler
from torcms.handlers.maintain_handler import MaintainCategoryHandler, MaintainCategoryAjaxHandler
from torcms.handlers.maintain_info_handler import MaintainPycateCategoryHandler
from torcms.handlers.page_handler import PageHandler
from torcms.handlers.page_ajax_handler import PageAjaxHandler
from torcms.handlers.post_handler import PostHandler
from torcms.handlers.post_ajax_handler import PostAjaxHandler
from torcms.handlers.reply_handler import ReplyHandler
from torcms.handlers.search_handler import SearchHandler
from torcms.handlers.user_handler import UserHandler, UserAjaxHandler
from torcms.handlers.wiki_handler import WikiHandler

from torcms.handlers.user_info_list_handler import UserListHandler
from torcms.handlers.collect_handler import CollectHandler
from torcms.handlers.evaluation_handler import EvaluationHandler
from torcms.handlers.post_info_relation_handler import RelHandler

from torcms.handlers.post_manager import PostManHandler
from torcms.handlers.wiki_manager import WikiManHandler
from torcms.handlers.rating_handler import RatingHandler

from torcms.handlers.geojson import GeoJsonHandler
from torcms.handlers.map_layout_handler import MapLayoutHandler
from torcms.handlers.map_handler import MapPostHandler
from torcms.handlers.map_overlay_handler import MapOverlayHandler
from torcms.handlers.admin_post_handler import AdminPostHandler

urls = [

    ('/map/overlay/(.*)', MapOverlayHandler, dict()),
    ("/map/(.*)", MapPostHandler, dict(kind='m')),
    ("/admin_post/(.*)", AdminPostHandler, dict()),
    ('/geojson/(.*)', GeoJsonHandler, dict()),
    ('/layout/(.*)', MapLayoutHandler, dict()),

    ('/_rating/(.*)', RatingHandler, dict()),
    ('/post_man/(.*)', PostManHandler, dict()),
    ('/meta_man/(.*)', PostManHandler, dict()),
    ('/wiki_man/(.*)', WikiManHandler, dict()),
    ('/page_man/(.*)', WikiManHandler, dict()),
    ("/label/(.*)", PostLabelHandler, dict()),
    ("/admin/(.*)", AdminHandler, dict()),
    ("/entry/(.*)", EntityHandler, dict()),
    ("/entity/(.*)", EntityHandler, dict()),
    ("/category/(.*)", CategoryHandler, dict()),
    ("/user/p/(.*)", UserAjaxHandler, dict()),  # Deprecated
    ("/user_j/(.*)", UserAjaxHandler, dict()),
    ("/user/(.*)", UserHandler, dict()),
    ("/post_j/(.*)", PostAjaxHandler, dict()),
    ("/post/p/(.*)", PostAjaxHandler, dict()),  # Deprecated,
    ("/post/(.*)", PostHandler, dict()),

    ("/maintain/p/category/(.*)", MaintainCategoryAjaxHandler, dict()),
    ("/maintain/category/(.*)", MaintainCategoryHandler, dict()),
    ("/link/p/(.*)", LinkHandler, dict()), # deprecated
    ("/link_j/(.*)", LinkHandler, dict()),
    ("/link/(.*)", LinkHandler, dict()),

    ("/page/p/(.*)", PageAjaxHandler, dict()),  # Deprecated
    ("/page_j/(.*)", PageAjaxHandler, dict()),
    ("/page/(.*)", PageHandler, dict()),
    ("/wiki/(.*)", WikiHandler, dict()),
    ("/search/(.*)", SearchHandler, dict()),
    ("/reply/(.*)", ReplyHandler, dict()),

    ("/info/(.*)", InfoHandler, dict(kind='9')),

    ("/maintain/claslitecategory/(.*)", MaintainPycateCategoryHandler, dict()),
    ("/list/(.*)", InfoListHandler, dict()),
    ("/publish/(.*)", InfoPublishHandler, dict()),

    ("/tag/(.*)", InforCategoryHandler, dict()),
    ('/info_tag/(.*)', InfoTagHandler, dict(hinfo={})),

    ("/collect/(.*)", CollectHandler, dict()),
    ('/rel/(.*)', RelHandler, dict()),
    ("/user_list/(.*)", UserListHandler, dict()),

    ("/evaluate/(.*)", EvaluationHandler, dict()),
    ("/", IndexHandler, dict()),

]
