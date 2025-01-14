from import_export import resources

from ..zn_event_category.models import ZNEvent
from django.contrib.auth import get_user_model

User = get_user_model()


class DataResource(resources.ModelResource):
    class Meta:
        model = ZNEvent
        import_id_fields = ['id']

