# -*- coding:utf-8 -*-

"""
Config for the website.
"""
from pathlib import Path

import tornado.web

from torcms.core.tools import get_cfg

try:
    from cfg import ADDONS
except:
    ADDONS = []

DB_CON, SMTP_CFG, SITE_CFG, ROLE_CFG, REDIS_CFG = get_cfg()

BaseDir = Path(__file__).resolve().parent

CMS_CFG = {
    "list_num": 10,
    "redis_kw": "lsadfkj",
    'expires_minutes': 60,
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

post_cfg = {
    "1": {
        "router": "post",
        "html": """<span style="color:green;" class="glyphicon glyphicon-list-alt">[{0}]</span>""".format(
            "Document"
        ),
        "checker": "1",
        "show": "Document",
    },
    "2": {
        "router": "page",
        "html": """<span style="color:green; glyphicon glyphicon-list-alt"></span> [{0}]</span>""".format(
            "Page"
        ),
        "checker": "0",
        "show": "Page",
    },
    "3": {
        "router": "info",
        "html": """<span style="color:blue;" class="glyphicon glyphicon-list-alt">[{0}]</span>""".format(
            "Info"
        ),
        "checker": "0",  # '10', '100', '1000', '10000'
        "show": "Info",
    },
    "k": {
        "router": "tutorial",
        "html": """<span style="color:blue;" class="glyphicon glyphicon-list-alt">[{0}]</span>""".format(
            "Tutorial"
        ),
        "checker": "0",  # '10', '100', '1000', '10000'
        "show": "Tutorial",
    },
}

ADDONS = ['torcms_app', 'torcms_maplet'] + ADDONS

for wdir in ADDONS:
    the_mod = f"{wdir}._config"
    _mod = __import__(the_mod)
    post_cfg = dict(post_cfg, **_mod._config._post_cfg)


class WidgetMenu(tornado.web.UIModule):
    """
    Get page info by page_id.
    """

    def render(self, *args, **kwargs):
        """ """
        out_str = ""

        tmpl = '<li class="nav-item"><a class="nav-link " aria-current="page" href="/{}/">{}</a></li>'
        ii = 1
        for key in post_cfg:
            if key == '2':
                continue

            if post_cfg[key]['router'] == 'topic':
                tmpl = '<li class="nav-item"><a class="nav-link " aria-current="page" href="/list/{}">{}</a></li>'
            else:
                tmpl = '<li class="nav-item"><a class="nav-link " aria-current="page" href="/{}/">{}</a></li>'
            out_str = out_str + tmpl.format(
                post_cfg[key]['router'],
                post_cfg[key].get('show', post_cfg[key].get('router')),
            )

        return out_str


class PublishListMenu(tornado.web.UIModule):
    """
    Get page info by page_id.
    """

    def render(self, *args, **kwargs):
        """ """
        str = args[0]
        out_str = ""

        tmpl = '''<a href="/check/{}?kind={}" class="btn btn-xs btn-success">{}</a>
        '''

        for key in post_cfg:
            out_str = out_str + tmpl.format(
                str, key, post_cfg[key].get('show', post_cfg[key].get('router'))
            )

        return out_str


config_modules = {
    "widget_menu": WidgetMenu,
    "publish_list_menu": PublishListMenu,
}
