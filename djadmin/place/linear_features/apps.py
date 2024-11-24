from django.apps import AppConfig


class ApiAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'place.linear_features'
    verbose_name = '线状要素库'