from django.apps import AppConfig


class CategoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'data.categorys'
    verbose_name = '数据分类管理'