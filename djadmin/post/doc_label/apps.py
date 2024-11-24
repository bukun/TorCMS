from django.apps import AppConfig


class LabelsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'post.doc_label'
    verbose_name = '文档标签管理'