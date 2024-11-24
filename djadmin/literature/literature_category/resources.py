from import_export import resources

from .models import LiteratureCatagory
from django.contrib.auth import get_user_model

User = get_user_model()


class CategoryResource(resources.ModelResource):
    class Meta:
        model = LiteratureCatagory
        import_id_fields = ['name']

