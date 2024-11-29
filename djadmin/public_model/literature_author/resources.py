from import_export import resources

from .models import LiteratureAuthor
from django.contrib.auth import get_user_model

User = get_user_model()


class CategoryResource(resources.ModelResource):
    class Meta:
        model = LiteratureAuthor
        import_id_fields = ['name']

