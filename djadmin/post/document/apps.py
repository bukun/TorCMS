from django.apps import AppConfig


class DataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'post.document'
    verbose_name = '文档管理'