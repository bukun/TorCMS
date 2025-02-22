from django.contrib.auth import get_user_model
from import_export import resources

from qgis.qgis_map.models import zhongmengmapcategory

User = get_user_model()


class ZhongmengMapCategoryResource(resources.ModelResource):
    class Meta:
        model = zhongmengmapcategory
        import_id_fields = ['name']
