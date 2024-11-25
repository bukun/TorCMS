from import_export import resources

from .models import LiteratureDate
from django.contrib.auth import get_user_model

User = get_user_model()


class CategoryResource(resources.ModelResource):
    class Meta:
        model = LiteratureDate
        import_id_fields = ['pub_date']

