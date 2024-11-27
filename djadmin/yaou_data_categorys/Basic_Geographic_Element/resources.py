from import_export import resources

from .models import Basic_Geographic_Element_Category
from django.contrib.auth import get_user_model

User = get_user_model()


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Basic_Geographic_Element_Category
        import_id_fields = ['name']

