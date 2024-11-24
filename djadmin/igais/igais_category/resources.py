from import_export import resources

from .models import igaiscategory
from django.contrib.auth import get_user_model

User = get_user_model()


class IgaisCategoryResource(resources.ModelResource):
    class Meta:
        model = igaiscategory
        import_id_fields = ['id']

