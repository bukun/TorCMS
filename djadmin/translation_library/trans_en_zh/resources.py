from import_export import resources

from .models import TranslationENZH
from django.contrib.auth import get_user_model

User = get_user_model()


class ApiAppResource(resources.ModelResource):
    class Meta:
        model = TranslationENZH
        import_id_fields = ['id']

