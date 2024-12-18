from import_export import resources

from .models import iga_floor
from django.contrib.auth import get_user_model

User = get_user_model()


class IgafloorResource(resources.ModelResource):
    class Meta:
        model = iga_floor
        import_id_fields = ['id']

