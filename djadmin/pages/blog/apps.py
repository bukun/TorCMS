from django.apps import AppConfig


class PageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pages.blog'
    verbose_name = '博客管理'
