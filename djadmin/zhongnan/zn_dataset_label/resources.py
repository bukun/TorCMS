from import_export import resources

from ..zn_dataset_category.models import ZNDatasetLabel
from django.contrib.auth import get_user_model

User = get_user_model()


class LabelResource(resources.ModelResource):
    class Meta:
        model = ZNDatasetLabel
        import_id_fields = ['name']

