# -*- coding: utf-8 -*-
import scrapy

# 以下三行是在 Python2.x版本中解决乱码问题，Python3.x 版本的可以去掉
# import sys
#
# reload(sys)
# sys.setdefaultencoding("utf-8")
import re

import html2text as ht
from mySpider.items import ItcastItem
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.loader import ItemLoader
from crawl.crawl_source.models import CrawlSource
from crawl.crawl_label.models import CrawlLabel
from datetime import datetime


def htmlToMarkDown(html):
    text_maker = ht.HTML2Text()
    text_maker.bypass_tables = False
    text = text_maker.handle(html)
    return text


def format_date(date_time):
    format = '%b %d %Y'
    datetime_str = datetime.strptime(date_time, format)
    return datetime_str


class Opp2Spider(scrapy.Spider):
    name = 'tcmap'
    allowed_domains = ['tcmap.com.cn']

    source_title = '博雅地名分享网'
    CrawlSource.objects.update_or_create(title=source_title, defaults={
        'url': allowed_domains[0]
    })
    start_urls = []
    start_urls.append("http://www.tcmap.com.cn/")

    def parse(self, response):
        sel = Selector(response)

        item = ItcastItem()

        alinkList = sel.xpath('//a[@class="topmenu"]/@href').extract()

        for alink in alinkList:
            alink = "http://www.tcmap.com.cn" + alink
            yield Request(url=alink, callback=self.parse)

        item['title'] = sel.xpath('//h1/text()').extract_first()

        if item['title']:
            conXpath = sel.xpath('//div[@id="page_left"]')
            imgXpath = conXpath.xpath('.//img')

            cur_alink=conXpath.xpath('//a[@class="blue"]/@href')
            alinkList.extend(cur_alink)
            logo_src = sel.xpath('//table//img/@src').extract_first()
            if logo_src:
                item['logo'] = f'scrapy/imgs/full/' + logo_src.split("/")[-1]

            item['author'] = sel.xpath('//a[@class="UserLink-link"]/text()').extract_first()

            item['cnt_html'] = conXpath.extract_first()


            imgs = []
            imgs.append(logo_src)
            for src in imgXpath:

                isrc = src.xpath('@src').get()

                if isrc.startswith("http:"):
                    img_src = isrc
                    imgs.append(img_src)
                elif isrc.startswith("//"):
                    img_src = "http:" + isrc
                    imgs.append(img_src)

                img_name = isrc.split("/")[-1]



                pattern = re.compile(r'<img.*src="' + isrc + '".*>')
                re_con = f'<img src="/scrapy/imgs/full/{img_name}">'

                loc_con=re.compile(r'<div style="margin:3px 0 0 5px;"><a href="/">您现在的位置</a>.*</div>')
                pat_con=re.compile(r'<div.*class="ht">.*</div>')
                yd_con=re.compile(r'<div.*align="center".*>.*移动版.*</div>')
                t_con=re.compile(r'<div style="float:left;"><table.*>.*</table></div>')
                item['cnt_html'] = re.sub(pattern, re_con,  item['cnt_html'])
                item['cnt_html']= re.sub(loc_con, '', item['cnt_html']  )
                item['cnt_html'] = re.sub(yd_con, '',   item['cnt_html'] )
                item['cnt_html'] = re.sub(t_con, '',   item['cnt_html'] )
                item['cnt_html'] =re.sub(pat_con, '',  item['cnt_html'])


            item['memo'] = imgs

            item['cnt_md'] = htmlToMarkDown(item['cnt_html'])
            item['create_time'] = datetime.now()
            item['source'] = CrawlSource.objects.filter(title=self.source_title).first()
            item['crawlurl'] = response.url

            yield item

