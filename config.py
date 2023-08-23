# -*- coding:utf-8 -*-

"""
Config for the website.
"""
import tornado.web
from torcms.core.tools import get_cfg
from pathlib import Path

DB_CON, SMTP_CFG, SITE_CFG, ROLE_CFG, REDIS_CFG = get_cfg()

CMS_CFG = {
    "list_num": 10,
    "redis_kw": "lsadfkj",
    # 'expires_minutes': 1
    "pass_encrypt": ",.",
}

post_emails = ["118171@qq.com"]

email_cfg = {
    "title": "好久没登录了",
    "content": """<div>尊敬的会员，您好：</div>
        <div>　　感谢您在网站注册</div>
        <div>　　网站是一个在线计算工具的网站，网站不断地在创新、完善。</div>
        <div>　　注册并登陆后，用户可收藏常用的计算工具，系统也会自动记录使用过的应用，方便以后的使用。</div>
        """,
}

# router_post = {"1": "post", "3": "info", "q": "topic", "v": "map-show", "k": "tutorial"}

post_cfg = {
    "1": {
        "router": "post",
        "html": """<span style="color:green;" class="glyphicon glyphicon-list-alt">[{0}]</span>""".format(
            "Document"
        ),
        "checker": "1",
        "show": "Document"
    },
    "2": {
        "router": "page",
        "html": """<span style="color:green; glyphicon glyphicon-list-alt"></span> [{0}]</span>""".format(
            "Page"
        ),
        "checker": "0",
        "show": "Page"
    },
    "3": {
        "router": "info",
        "html": """<span style="color:blue;" class="glyphicon glyphicon-list-alt">[{0}]</span>""".format(
            "Info"
        ),
        "checker": "0",  # '10', '100', '1000', '10000'
        "show": "Info"
    },
    # "v": {
    #     "router": "map",
    #     "html": """<span style="color:red;" class="glyphicon glyphicon-globe">[{0}]</span>""".format(
    #         "Map"
    #     ),
    #     "checker": "0",  # '10', '100', '1000', '10000'
    #     "show": "Map"
    # },
    "k": {
        "router": "tutorial",
        "html": """<span style="color:blue;" class="glyphicon glyphicon-list-alt">[{0}]</span>""".format(
            "Tutorial"
        ),
        "checker": "0",  # '10', '100', '1000', '10000'
        "show": "Tutorial"
    },
    # "s": {
    #     "router": "app",
    #     "html": """<span style="color:blue;" class="glyphicon glyphicon-list-alt">[{0}]</span>""".format(
    #         "APP"
    #     ),
    #     "checker": "0",  # '10', '100', '1000', '10000'
    #     "show": "APP"
    # },
    # "q": {
    #     "router": "topic",
    #     "html": """<span style="color:blue;" class="glyphicon glyphicon-list-alt">[{0}]</span>""".format(
    #         "Topics"
    #     ),
    #     "checker": "0",  # '10', '100', '1000', '10000'
    #     "show": "Topics"
    # },
}

APP_MASK = ["g_drr", "9_todo_new", "9_todo_new5"]

# _mod = __import__('torcms_app._config')
# post_cfg = dict(post_cfg, **_mod._config._post_cfg)


for wdir in Path(".").iterdir():
    if wdir.is_dir() and wdir.name.startswith("torcms_"):
        the_file = f"{wdir.name}._config"
        print(the_file)
        _mod = __import__(the_file)
        post_cfg = dict(post_cfg, **_mod._config._post_cfg)


class WidgetMenu(tornado.web.UIModule):
    """
    Get page info by page_id.
    """

    def render(self, *args, **kwargs):
        """ """
        out_str = ""

        tmpl = '<li><a href="/{}/">{}</a></li>'
        ii = 1
        for key in post_cfg:
            if key =='2':
                continue

            if ii < 7:
                if post_cfg[key]['router'] == 'topic':
                    tmpl = '<li><a href="/list/{}">{}</a></li>'
                else:
                    tmpl = '<li><a href="/{}/">{}</a></li>'
                out_str = out_str + tmpl.format(
                    post_cfg[key]['router'],
                    post_cfg[key].get('show', post_cfg[key].get('router'))
                )
                ii = ii + 1
        return out_str


class PublishListMenu(tornado.web.UIModule):
    """
    Get page info by page_id.
    """

    def render(self, *args, **kwargs):
        """ """
        str = args[0]
        out_str = ""

        tmpl = '<a href="/check/{}?kind={}" class="btn btn-xs btn-success">{}</a>'

        for key in post_cfg:
            out_str = out_str + tmpl.format(str, key, post_cfg[key].get('show', post_cfg[key].get('router')))

        return out_str


config_modules = {
    "widget_menu": WidgetMenu,
    "publish_list_menu": PublishListMenu,
}
