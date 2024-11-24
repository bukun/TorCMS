from import_export import resources

from .models import Barndataset
from django.contrib.auth import get_user_model

User = get_user_model()


class BarndatasetResource(resources.ModelResource):
    class Meta:
        model = Barndataset
        import_id_fields = ['id']

