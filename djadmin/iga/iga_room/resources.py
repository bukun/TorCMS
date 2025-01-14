from import_export import resources

from iga.iga_group.models import iga_room
from django.contrib.auth import get_user_model

User = get_user_model()


class IgaroomResource(resources.ModelResource):
    class Meta:
        model = iga_room
        import_id_fields = ['id']

