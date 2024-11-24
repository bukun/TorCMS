from import_export import resources

from .models import Jupyter
from django.contrib.auth import get_user_model

User = get_user_model()


class JupyterResource(resources.ModelResource):
    class Meta:
        model = Jupyter
        import_id_fields = ['id']

