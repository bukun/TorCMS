# -*- coding:utf-8 -*-

'''
Config for the website.
'''
import tornado.web
from torcms.core.tools import get_cfg
from pathlib import Path

DB_CON, SMTP_CFG, SITE_CFG, ROLE_CFG, REDIS_CFG = get_cfg()

CMS_CFG = {
    'list_num': 10,
    'redis_kw': 'lsadfkj',
    # 'expires_minutes': 1
    'pass_encrypt': ',.',
}

post_emails = ['118171@qq.com']

email_cfg = {
    'title': '好久没登录了',
    'content':
        '''<div>尊敬的会员，您好：</div>
        <div>　　感谢您在“云算笔记”网站注册</div>
        <div>　　“云算笔记”网站是一个在线计算工具的网站，网站不断地在创新、完善。</div>
        <div>　　注册并登陆后，用户可收藏常用的计算工具，系统也会自动记录使用过的应用，方便以后的使用。</div>
        <p> </p>
        <div>　　根据我们的记录，您好久没有登录我们的网站了。</div>
        <div>　　如果希望回到我们网站，请打开链接<a href="http://www.yunsuan.org/user/login"> 登陆 </a>。</div>
        <div>　　如果忘记了用户名或密码，请打开链接
        <a href="http://www.yunsuan.org/user/reset-password"> 密码重置 </a>，输入Email即可。</div>
            '''
    ,
}

router_post = {
    '1': 'post',
    '3': 'info',
    'q': 'topic',
    'v': 'map-show',
    'k': 'tutorial'
}

post_type = {
    '1': '''<span style="color:green;" class="glyphicon glyphicon-list-alt">[{0}]</span>
        '''.format('Document'),
    '3': '''<span style="color:blue;" class="glyphicon glyphicon-list-alt">[{0}]</span>
        '''.format('Data'),
    'q': '''<span style="color:red;" class="glyphicon glyphicon-list-alt">[{0}]</span>
            '''.format('Topic'),
    'v': '''<span style="color:red;" class="glyphicon glyphicon-globe">[{0}]</span>
            '''.format('Map visualization'),
    'k': '''<span style="color:blue;" class="glyphicon glyphicon-list-alt">[{0}]</span>
        '''.format('Tutorial'),
}
check_type = {
    '1': 'Document',
    '3': 'Infor',
    'v': 'Map visualization',
    'k': 'Tutorial',
}
post_cfg = {
    '1': {
        'router': 'post',
        'html': '''<span style="color:green;" class="glyphicon glyphicon-list-alt">[{0}]</span>'''.format('Document'),
        'checker': '1',
    },
    '3': {
        'router': 'info',
        'html': '''<span style="color:blue;" class="glyphicon glyphicon-list-alt">[{0}]</span>'''.format('Data'),
        'checker': '10',  # '10', '100', '1000', '10000'
    },
    'v': {
        'router': 'info',
        'html': '''<span style="color:red;" class="glyphicon glyphicon-globe">[{0}]</span>'''.format('Map visualization'),
        'checker': '0',  # '10', '100', '1000', '10000'
    },
    'k': {
        'router': 'tutorial',
        'html': '''<span style="color:blue;" class="glyphicon glyphicon-list-alt">[{0}]</span>'''.format('Tutorial'),
        'checker': '10',  # '10', '100', '1000', '10000'
    }

}
kind_arr = ['1', '3', 'm', 's', 'q', 'v']
APP_MASK = ['g_drr', '9_todo_new', '9_todo_new5']
for wdir in Path('.').iterdir():
    if wdir.is_dir() and wdir.name.startswith('torcms_'):
        the_file = f'{wdir.name}._config'
        print(the_file)
        _mod = __import__(the_file)
        router_post = dict(router_post, **_mod._config._router_post)
        post_type = dict(post_type, **_mod._config._post_type)
        check_type = dict(check_type, **_mod._config._check_type)
        post_cfg = dict(post_cfg, **_mod._config._post_cfg)
        # kind_arr = kind_arr + _mod.config._kind_arr


class WidgetMenu(tornado.web.UIModule):
    '''
    Get page info by page_id.
    '''

    def render(self, *args, **kwargs):
        '''
        '''
        out_str = ''

        tmpl = '<li><a href="/{}/">{}</a></li>'

        for key in check_type:
            out_str = out_str + tmpl.format(router_post[key], check_type[key])

        return out_str


class PublishListMenu(tornado.web.UIModule):
    '''
    Get page info by page_id.
    '''

    def render(self, *args, **kwargs):
        '''
        '''
        str = args[0]
        out_str = ''

        tmpl = ' <a href="/check/{}?kind={}" class="btn btn-xs btn-success">{}</a>'

        for key in check_type:
            out_str = out_str + tmpl.format(str, key, check_type[key])

        return out_str


config_modules = {
    'widget_menu': WidgetMenu,
    'publish_list_menu': PublishListMenu,
}
