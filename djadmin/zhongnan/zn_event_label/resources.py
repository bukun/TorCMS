from import_export import resources

from ..zn_event_category.models import ZNEventLabel
from django.contrib.auth import get_user_model

User = get_user_model()


class LabelResource(resources.ModelResource):
    class Meta:
        model = ZNEventLabel
        import_id_fields = ['name']

