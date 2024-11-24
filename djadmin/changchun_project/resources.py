from import_export import resources

from .models import ChangChunProject
from django.contrib.auth import get_user_model

User = get_user_model()


class ChangChunProjectResource(resources.ModelResource):
    class Meta:
        model = ChangChunProject
        import_id_fields = ['title']

