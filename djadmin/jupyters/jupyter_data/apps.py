from django.apps import AppConfig


class JupyterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'jupyters.jupyter_data'
    verbose_name = '科学计算模型管理'