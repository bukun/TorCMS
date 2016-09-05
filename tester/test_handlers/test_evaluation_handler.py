# -*- coding:utf-8 -*-

from torcms.handlers.evaluation_handler import EvaluationHandler


def Test():
    # assert InfoHandler(dict(), request="/entity/(.*)")
    urls = [
        ("/label/(.*)", EvaluationHandler, dict()), ]
    assert urls
