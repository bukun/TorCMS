from django.apps import AppConfig


class DataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crawl.crawl_document'
    verbose_name = '爬取文档管理'