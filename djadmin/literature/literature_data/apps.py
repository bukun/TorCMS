from django.apps import AppConfig


class literatureConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'literature.literature_data'
    verbose_name = '文献数据管理'