from django.apps import AppConfig


class ApiAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'place.planar_features'
    verbose_name = '面状要素库'