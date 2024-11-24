from import_export import resources

from .models import farmproavg
from django.contrib.auth import get_user_model

User = get_user_model()


class FarmproAvgResource(resources.ModelResource):
    class Meta:
        model = farmproavg
        import_id_fields = ['product_name']

