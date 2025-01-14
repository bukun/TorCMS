from django.apps import AppConfig


class ApiAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'translation_library.trans_en_zh'
    verbose_name = '翻译管理'