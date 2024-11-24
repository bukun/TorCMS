from import_export import resources

from .models import JupyterCatagory
from django.contrib.auth import get_user_model

User = get_user_model()


class JupyterCatagoryResource(resources.ModelResource):
    class Meta:
        model = JupyterCatagory
        import_id_fields = ['name']

