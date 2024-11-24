from import_export import resources

from .models import Soilfivepara1
from django.contrib.auth import get_user_model

User = get_user_model()


class Soilfivepara1Resource(resources.ModelResource):
    class Meta:
        model = Soilfivepara1
        import_id_fields = ['id']

