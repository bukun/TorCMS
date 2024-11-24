from import_export import resources

from .models import TestText
from django.contrib.auth import get_user_model

User = get_user_model()


class TestTextResource(resources.ModelResource):
    class Meta:
        model = TestText
        import_id_fields = ['id']

