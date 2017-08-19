# -*- coding:utf-8 -*-

from torcms.handlers.category_maintain_handler import MaintainCategoryAjaxHandler, MaintainCategoryHandler


def Test():
    urls = [
        ("/label/(.*)", MaintainCategoryAjaxHandler, dict()),
        ("/label/(.*)", MaintainCategoryHandler, dict()),
    ]

    assert urls
