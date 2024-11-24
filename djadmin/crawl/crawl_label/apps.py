from django.apps import AppConfig


class CrawlLabelsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crawl.crawl_label'
    verbose_name = '爬取文档标签管理'