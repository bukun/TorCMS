from import_export import resources

from data.categorys.models import dataset
from django.contrib.auth import get_user_model

User = get_user_model()


class DataResource(resources.ModelResource):
    class Meta:
        model = dataset
        import_id_fields = ['id']

