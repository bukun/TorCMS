from django.contrib.auth import get_user_model
from import_export import resources

from qgis.qgis_map.models import zhongbamapcategory

User = get_user_model()


class ZhongbaMapCategoryResource(resources.ModelResource):
    class Meta:
        model = zhongbamapcategory
        import_id_fields = ['name']
