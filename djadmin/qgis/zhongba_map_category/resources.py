from import_export import resources

from .models import zhongbamapcategory
from django.contrib.auth import get_user_model

User = get_user_model()


class ZhongbaMapCategoryResource(resources.ModelResource):
    class Meta:
        model = zhongbamapcategory
        import_id_fields = ['name']

