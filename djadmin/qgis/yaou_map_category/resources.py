from import_export import resources

from .models import yaoumapcategory
from django.contrib.auth import get_user_model

User = get_user_model()


class YaouMapCategoryResource(resources.ModelResource):
    class Meta:
        model = yaoumapcategory
        import_id_fields = ['id']

