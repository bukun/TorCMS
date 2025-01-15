from import_export import resources

from ..igais_category.models import igaislabel
from django.contrib.auth import get_user_model

User = get_user_model()


class IgaisLabelResource(resources.ModelResource):
    class Meta:
        model = igaislabel
        import_id_fields = ['name']

