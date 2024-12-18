from import_export import resources

from .models import iga_staff
from django.contrib.auth import get_user_model

User = get_user_model()


class IgastaffResource(resources.ModelResource):
    class Meta:
        model = iga_staff
        import_id_fields = ['id']

