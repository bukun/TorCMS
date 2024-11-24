# Scrapy settings for mySpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath('.')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'  # 项目名.settings
import django

django.setup()
from pathlib import Path

BOT_NAME = "mySpider"

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SPIDER_MODULES = ["mySpider.spiders"]
NEWSPIDER_MODULE = "mySpider.spiders"

HTTPERROR_ALLOWED_CODES = [403]
FILES_STORE = os.path.join(BASE_DIR, 'static/img/scrapy/files/')
IMAGES_STORE = os.path.join(BASE_DIR, 'static/img/scrapy/imgs/')

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0"


# Obey robots.txt rules
ROBOTSTXT_OBEY = False  # 是否遵循机器人协议，默认是true，需要改为false，否则很多东西爬不了

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    'Cookie': 'adb_isBlock=0; userid=1652710683278_ihrfq92084; prov=cn0731; city=0732; weather_city=hn_xt; region_ip=110.53.149.x; region_ver=1.2; wxIsclose=false; ifengRotator_iis3=6; ifengWindowCookieName_919=1'
    # 默认是注释的，这个东西非常重要，如果不写很容易被判断为电脑，简单点洗一个Mozilla/5.0即可

}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    "mySpider.middlewares.MyspiderSpiderMiddleware": 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    "mySpider.middlewares.MyspiderDownloaderMiddleware": 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "mySpider.pipelines.MyspiderPipeline": 300,
    "mySpider.pipelines.MyImagesPipeline": 200,
    "mySpider.pipelines.PdfPipeline": 200,

}
# 避免下载最近90天已经下载过的文件内容
FILES_EXPIRES = 90
# 90天的图片失效期限
IMAGES_EXPIRES = 90
# 图片最小高度和宽度设置，可以过滤太小的图片
# IMAGES_MIN_HEIGHT = 110
# IMAGES_MIN_WIDTH = 110
# 缩略图
IMAGES_THUMBS = {
    'small': (270, 270),
    'big': (500, 500),
}
# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = "httpcache"
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
