# -*- coding:utf-8 -*-


from torcms.handlers.admin_handler import AdminHandler



def Test():
    # assert InfoHandler(dict(), request="/entity/(.*)")
    urls = [ ("/label/(.*)", AdminHandler, dict()), ]
    assert urls

