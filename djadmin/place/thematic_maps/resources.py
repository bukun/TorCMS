from import_export import resources

from .models import ThematicMaps
from django.contrib.auth import get_user_model

User = get_user_model()


class ThematicMapsResource(resources.ModelResource):
    class Meta:
        model = ThematicMaps
        import_id_fields = ['layer']

