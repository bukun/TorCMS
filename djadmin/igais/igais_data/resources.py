from import_export import resources

from .models import igaisdata
from django.contrib.auth import get_user_model

User = get_user_model()


class IgaisDataResource(resources.ModelResource):
    class Meta:
        model = igaisdata
        import_id_fields = ['title']

