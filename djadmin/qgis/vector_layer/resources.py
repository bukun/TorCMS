from import_export import resources

from .models import vectorlayer
from django.contrib.auth import get_user_model

User = get_user_model()


class vectorlayerResource(resources.ModelResource):
    class Meta:
        model = vectorlayer
        import_id_fields = ['mapid']

