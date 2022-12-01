# -*- coding:utf-8 -*-

'''
Config for the website.
'''
from torcms.core.tools import get_cfg

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

router_post = {'1': 'post',
               }

post_type = {
    '1': '''<span style="color:green;" class="glyphicon glyphicon-list-alt">[{0}]</span>
        '''.format('Document'),
}
check_type = {
    '1': 'Document',
}
post_cfg = {
    '1': {
        'router': 'post',
        'html': '''<span style="color:green;" class="glyphicon glyphicon-list-alt">[{0}]</span>'''.format('Document'),
        'checker': '1',
    },


}
kind_arr = ['1','9','m','s']

from pathlib import Path

for wdir in Path('.').iterdir():
    if wdir.is_dir() and wdir.name.startswith('torcms_'):
        the_file = f'{wdir.name}.config'
        print(the_file)
        _mod = __import__(the_file)

        router_post = dict(router_post, **_mod.config._router_post)
        post_type = dict(post_type, **_mod.config._post_type)
        check_type = dict(check_type, **_mod.config._check_type)
        post_cfg = dict(post_cfg, **_mod.config._post_cfg)
        # kind_arr = kind_arr + _mod.config._kind_arr
