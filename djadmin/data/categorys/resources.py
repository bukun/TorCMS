from import_export import resources

from .models import categorys
from django.contrib.auth import get_user_model

User = get_user_model()


class CategoryResource(resources.ModelResource):
    class Meta:
        model = categorys
        import_id_fields = ['name']

