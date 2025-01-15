from import_export import resources

from ..barn_dataset.models import Meteorology
from django.contrib.auth import get_user_model

User = get_user_model()


class MeteorologyResource(resources.ModelResource):
    class Meta:
        model = Meteorology
        import_id_fields = ['id']

