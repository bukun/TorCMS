from import_export import resources

from .models import map
from django.contrib.auth import get_user_model

User = get_user_model()


class MapResource(resources.ModelResource):
    class Meta:
        model = map
        import_id_fields = ['id']

