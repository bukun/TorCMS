from import_export import resources

from .models import apiapp
from django.contrib.auth import get_user_model

User = get_user_model()


class ApiAppResource(resources.ModelResource):
    class Meta:
        model = apiapp
        import_id_fields = ['title']

