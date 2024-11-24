from django.apps import AppConfig


class CrawlSourceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crawl.crawl_source'
    verbose_name = '爬取数据来源管理'