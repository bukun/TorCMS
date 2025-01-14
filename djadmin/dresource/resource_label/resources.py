from import_export import resources

from dresource.resource_category.models import ResourceLabel
from django.contrib.auth import get_user_model

User = get_user_model()


class LabelResource(resources.ModelResource):
    class Meta:
        model = ResourceLabel
        import_id_fields = ['name']

