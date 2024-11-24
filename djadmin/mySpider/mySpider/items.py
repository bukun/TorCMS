# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

from crawl.crawl_document_en import models
# from crawl.crawl_document import models
from scrapy_djangoitem import DjangoItem


class MyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ItcastItem(DjangoItem):
    label = scrapy.Field()
    django_model = models.CrawlDocumentEN  # 注入django项目的固定写法，必须起名为django_model =django中models.ABCkg表
    # django_model = models.CrawlDocument  # 注入django项目的固定写法，必须起名为django_model =django中models.ABCkg表
