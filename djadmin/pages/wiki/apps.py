from django.apps import AppConfig


class WikiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pages.wiki'
    verbose_name = '维基管理'
