from import_export import resources

from .models import iga_group
from django.contrib.auth import get_user_model

User = get_user_model()


class IgagroupResource(resources.ModelResource):
    class Meta:
        model = iga_group
        import_id_fields = ['id']

