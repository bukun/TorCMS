from import_export import resources

from .models import ResourceCatagory
from django.contrib.auth import get_user_model

User = get_user_model()


class CategoryResource(resources.ModelResource):
    class Meta:
        model = ResourceCatagory
        import_id_fields = ['name']

