from import_export import resources

from ..barn_dataset.models import Devicesoilmoisture
from django.contrib.auth import get_user_model

User = get_user_model()


class DevicesoilmoistureResource(resources.ModelResource):
    class Meta:
        model = Devicesoilmoisture
        import_id_fields = ['id']

