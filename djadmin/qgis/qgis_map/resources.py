from django.contrib.auth import get_user_model
from import_export import resources

from .models import qgismap

User = get_user_model()


class QgisMapResource(resources.ModelResource):
    class Meta:
        model = qgismap
        import_id_fields = ['mapid']
