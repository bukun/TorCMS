from django.contrib.auth import get_user_model
from import_export import resources

from qgis.qgis_map.models import heitumapcategory

User = get_user_model()


class HeituMapCategoryResource(resources.ModelResource):
    class Meta:
        model = heitumapcategory
        import_id_fields = ['name']
