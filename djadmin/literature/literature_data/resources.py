from import_export import resources

from .models import Literature
from django.contrib.auth import get_user_model

User = get_user_model()


class literatureResource(resources.ModelResource):
    class Meta:
        model = Literature
        import_id_fields = ['id']

