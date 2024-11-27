from django.apps import AppConfig


class LabelsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'data.labels'
    verbose_name = '数据标签管理'