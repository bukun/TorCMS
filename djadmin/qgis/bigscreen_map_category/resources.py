from import_export import resources

from qgis.qgis_map.models import BigScreenMapCategory
from django.contrib.auth import get_user_model

User = get_user_model()


class BigScreenMapCategoryResource(resources.ModelResource):
    class Meta:
        model = BigScreenMapCategory
        import_id_fields = ['name']

