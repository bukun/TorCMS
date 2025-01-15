from import_export import resources

from ..barn_dataset.models import Barndevice
from django.contrib.auth import get_user_model

User = get_user_model()


class BarndeviceResource(resources.ModelResource):
    class Meta:
        model = Barndevice
        import_id_fields = ['id']

