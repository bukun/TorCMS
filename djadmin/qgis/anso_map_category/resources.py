from import_export import resources

from qgis.qgis_map.models import ANSOMapCategory
from django.contrib.auth import get_user_model

User = get_user_model()


class ANSOMapCategoryResource(resources.ModelResource):
    class Meta:
        model = ANSOMapCategory
        import_id_fields = ['id']

