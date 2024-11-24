from import_export import resources

from .models import BigScreenData
from django.contrib.auth import get_user_model

User = get_user_model()


class BigScreenResource(resources.ModelResource):
    class Meta:
        model = BigScreenData
        import_id_fields = ['title']

