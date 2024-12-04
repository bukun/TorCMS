from import_export import resources

from .models import Photoinfo
from django.contrib.auth import get_user_model

User = get_user_model()


class PhotoinfoResource(resources.ModelResource):
    class Meta:
        model = Photoinfo
        import_id_fields = ['id']

