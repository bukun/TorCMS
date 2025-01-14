from import_export import resources

from qgis.qgis_map.models import QgisLabel
from django.contrib.auth import get_user_model

User = get_user_model()


class LabelResource(resources.ModelResource):
    class Meta:
        model = QgisLabel
        import_id_fields = ['name']

