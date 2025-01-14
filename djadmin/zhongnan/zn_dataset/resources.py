from import_export import resources

from ..zn_dataset_category.models import ZNDataset
from django.contrib.auth import get_user_model

User = get_user_model()


class DataResource(resources.ModelResource):
    class Meta:
        model = ZNDataset
        import_id_fields = ['id']

