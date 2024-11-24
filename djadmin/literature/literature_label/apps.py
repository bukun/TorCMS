from django.apps import AppConfig


class LabelsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'literature.literature_label'
    verbose_name = '文献标签管理'