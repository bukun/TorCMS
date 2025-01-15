from import_export import resources

from ..barn_dataset.models import Barnfield
from django.contrib.auth import get_user_model

User = get_user_model()


class BarnfieldResource(resources.ModelResource):
    class Meta:
        model = Barnfield
        import_id_fields = ['id']

