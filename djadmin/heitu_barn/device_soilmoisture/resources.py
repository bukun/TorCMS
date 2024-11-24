from import_export import resources

from .models import Devicesoilmoisture
from django.contrib.auth import get_user_model

User = get_user_model()


class DevicesoilmoistureResource(resources.ModelResource):
    class Meta:
        model = Devicesoilmoisture
        import_id_fields = ['id']

