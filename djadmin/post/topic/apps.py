from django.apps import AppConfig


class DataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'post.topic'
    verbose_name = '问答管理'