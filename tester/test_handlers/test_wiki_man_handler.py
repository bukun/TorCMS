# -*- coding:utf-8 -*-

from torcms.handlers.wiki_history_manager import WikiHistoryHandler


def Test():
    urls = [
        ("/wiki_man/(.*)", WikiHistoryHandler, dict()),
    ]
    assert urls
