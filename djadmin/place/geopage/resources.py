from import_export import resources

from .models import GeoPage
from django.contrib.auth import get_user_model

User = get_user_model()


class GeoPageResource(resources.ModelResource):
    class Meta:
        model = GeoPage
        import_id_fields = ['id']
