from import_export import resources

from data.categorys.models import labels
from django.contrib.auth import get_user_model

User = get_user_model()


class LabelResource(resources.ModelResource):
    class Meta:
        model = labels
        import_id_fields = ['name']

