from import_export import resources

from .models import farmpro
from django.contrib.auth import get_user_model

User = get_user_model()


class FarmproResource(resources.ModelResource):
    class Meta:
        model = farmpro
        import_id_fields = ['product_name']

