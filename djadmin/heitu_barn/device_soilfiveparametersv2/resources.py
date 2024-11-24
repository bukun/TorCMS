from import_export import resources

from .models import Soilfiveparav2
from django.contrib.auth import get_user_model

User = get_user_model()


class Soilfiveparav2Resource(resources.ModelResource):
    class Meta:
        model = Soilfiveparav2
        import_id_fields = ['id']

