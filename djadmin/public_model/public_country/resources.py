from import_export import resources
from public_model.literature_author.models import PublicCountry
from django.contrib.auth import get_user_model

User = get_user_model()


class CategoryResource(resources.ModelResource):
    class Meta:
        model = PublicCountry
        import_id_fields = ['name']

