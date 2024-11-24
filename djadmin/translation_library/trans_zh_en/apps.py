from django.apps import AppConfig


class ApiAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'translation_library.trans_zh_en'
    verbose_name = '中-英翻译'