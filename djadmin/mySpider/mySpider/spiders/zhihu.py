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




    name = 'zhihu'
    allowed_domains = ['zhihu.com']

    source_title = '知乎'
    CrawlSource.objects.update_or_create(title=source_title, defaults={
        'url': allowed_domains[0]
    })
    start_urls = []
    # for page in range(2, 3):
    #     start_urls.append(f'https://www.zhihu.com/people/hao-jin-fan-hua/posts?page={page}')

    start_urls.append("https://www.zhihu.com/people/hao-jin-fan-hua/posts?page=2")

    def start_requests(self):
        headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': '_xsrf=6cd9a6f3-2229-4f2f-9447-cd145d4a1216; YD00517437729195%3AWM_TID=ErD12XfEMM5BAFQEABbUbA81nU4g5cm4; __snaker__id=MtGfNS0qHujluNUP; b-user-id=0ef78d7a-695d-df7e-f7e9-9c8c9cf7de69; o_act=login; ref_source=other_https://www.zhihu.com/signin?next=/; expire_in=15551999; q_c1=0f3ebd07d3754273901b99f96e20cbe8|1698370016000|1698370016000; YD00517437729195%3AWM_NI=m5VZghLDPxRxLirTH2DJ8jpynFHPaUZxvynfODwp49XWd0V48SByI%2F6yTgvCLeWPeLHceEfrTIulPdi2QM3JttPzmKk%2FXiN4sC8rt9bACniYWwxq8TAwmWg8PLygB2vsTGY%3D; YD00517437729195%3AWM_NIKE=9ca17ae2e6ffcda170e2e6ee96f464908d0098f33a9cb08eb7c15f969a8eb1d43ab2ecb891c14eadaebab7bb2af0fea7c3b92aafeb9abbe664909ca099d17490b7beb5cb3a8896f88bf373ae9a88b1e45f9aa8ba9aed6e8d9cb991b7339c89acd1d540fc8d8e9acc25f6a79c88f54990bb99b1e8488cbdaba6e57a9897bb8dd370abee9faeb242b8aca09bf041a9f1988acd40b19df893f733a29f8d8fec5395a9b892bb6083a9a3b8e6349494b788c13ab6ad9ca8dc37e2a3; _zap=3f28e9f1-b1ca-425b-8f96-30fece870ba0; d_c0=AOCZC2o4exiPTmV7_9UaaEAsjV-Gqk7R59U=|1713366039; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1713366042; z_c0=2|1:0|10:1714986799|4:z_c0|80:MS4xVXNmTEVnQUFBQUFtQUFBQVlBSlZUUm95RFdlLWlrQWRocFduSVdDOUptVkdSSUxVU3EzcGVBPT0=|ff5309ffd2162350b7efcbe1a528299f678191dbc977359aac26779a138ac9b6; BEC=d5e2304fff7e4240174612484fe7ffa4; SESSIONID=RKulS0VvcJXRxaUPNCf5BFQAhugk1sI2rJpnxkaVLkp; JOID=W1wWBENMYCNuVL_sFUJcPqwija0JEyxSDQaCvWcuJ3w4I9-0QuOiEAZYte8eVHwArboq2jZXsB1EzmXzD7CF26A=; osd=UF0dBkhHYShsX7TtHkBXNa0pj6YCEidQBg2DtmUlLH0zIdS_Q-igGw1Zvu0VX30Lr7Eh2z1VuxZFxWf4BLGO2as=; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1714995753; tst=r; KLBRSID=c450def82e5863a200934bb67541d696|1714995755|1714995616; BAIDU_SSP_lcr=https://www.baidu.com/link?url=QDCkdmq_2Wsk8fmXoEsi1I5_Zx8pl5Rm7FANw5Jug0G&wd=&eqid=93e964760018a40a000000066638c19d',
            'priority': 'u=1, i',
            'referer': 'https://www.zhihu.com/',
            'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'x-api-version': '3.0.53',
            'x-requested-with': 'fetch',
            'x-zse-93': '101_3_3.0',
            'x-zse-96': '2.0_d12mG68K1ljV2BZnPhwPUQDOMLexjCRJBTqpPsxNicPmzZ1KC3gIK1SjH4P=vP4D',
            'x-zst-81': '3_2.0aR_sn77yn6O92wOB8hPZnQr0EMYxc4f18wNBUgpTQ6nxERFZKTY0-4Lm-h3_tufIwJS8gcxTgJS_AuPZNcXCTwxI78YxEM20s4PGDwN8gGcYAupMWufIeQuK7AFpS6O1vukyQ_R0rRnsyukMGvxBEqeCiRnxEL2ZZrxmDucmqhPXnXFMTAoTF6RhRuLPF7V1phOf8gL_e8cfjUeBJw39pqLCFgXKYuwCghCB0rS0LrHKIDXKW9CKo0rTv0ofk4e9NhXqNcpKxDgLcBC0_ht1wcUM0uYx8Bw0sB3Orec93gSu9vcLygHKQTxYACc9e9H0qhLLHqL9tgwpaup0ZbXOPwXfe9Cp8qp1bgwfiwH_HutmCqfzqwo0xwN8PGFmJDo9yhLGYup9kMS80wV_K6xOVCLBewNLuGHmgvLLJ4XGI9Fp8rLmFGgGuqCLPUgLYCX95JL1DbrfyCgYCBLGkrXOk9O1BGHVCweCK8CC',
        }

    def parse(self, response):
        sel = Selector(response)

        item = ItcastItem()

        item['title'] = sel.xpath('//h1[@class="Post-Title"]/text()').extract_first()
        print("/" * 50)
        print(item['title'])
        if item['title']:
            conXpath = sel.xpath('//div[@class="css-1od93p9"]')
            imgXpath = conXpath.xpath('.//img')
            update_time = sel.xpath('//div[@class="ContentItem-time"]/text()').extract_first()

            logo_src = sel.xpath('//picture/img/@src').extract_first()
            if logo_src:
                item['logo'] = f'scrapy/imgs/full/' + logo_src.split("/")[-1]

            item['author'] = sel.xpath('//a[@class="UserLink-link"]/text()').extract_first()

            item['cnt_html'] = conXpath.extract_first()


            imgs = []
            imgs.append(logo_src)
            for src in imgXpath:

                isrc = src.xpath('@src').get()

                if isrc.startswith("https:"):
                    img_src = isrc
                    imgs.append(img_src)
                elif isrc.startswith("//"):
                    img_src = "https:" + isrc
                    imgs.append(img_src)

                img_name = isrc.split("/")[-1]



                pattern = re.compile(r'<img.*src="' + isrc + '".*>')
                re_con = f'<img src="/scrapy/imgs/full/{img_name}">'
                item['cnt_html'] = re.sub(pattern, re_con, item['cnt_html'])

            item['memo'] = imgs

            item['cnt_md'] = htmlToMarkDown(item['cnt_html'])
            item['create_time'] = datetime.now()
            item['update_time'] = update_time
            item['source'] = CrawlSource.objects.filter(title=self.source_title).first()
            item['crawlurl'] = response.url

            yield item

        alinkList = sel.xpath('//h2[@class="ContentItem-title"]/span/a/@href').extract()
        print("-" * 50)
        print(alinkList)
        for alink in alinkList:
            print("*" * 10)
            print(alink)
            alink="https:"+alink
            yield Request(url=alink, callback=self.parse)


