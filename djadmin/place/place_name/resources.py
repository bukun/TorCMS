from import_export import resources

from .models import PlaceName
from django.contrib.auth import get_user_model

User = get_user_model()


class ApiAppResource(resources.ModelResource):
    class Meta:
        model = PlaceName
        import_id_fields = ['id']
