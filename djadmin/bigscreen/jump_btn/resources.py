from import_export import resources

from .models import JumpBtn
from django.contrib.auth import get_user_model

User = get_user_model()


class BigScreenResource(resources.ModelResource):
    class Meta:
        model = JumpBtn
        import_id_fields = ['name']

