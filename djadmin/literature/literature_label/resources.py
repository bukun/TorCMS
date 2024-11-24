from import_export import resources

from .models import LiteratureLabel
from django.contrib.auth import get_user_model

User = get_user_model()


class LabelResource(resources.ModelResource):
    class Meta:
        model = LiteratureLabel
        import_id_fields = ['name']

