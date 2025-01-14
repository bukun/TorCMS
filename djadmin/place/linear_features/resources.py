from import_export import resources

from place.geofea.models  import LinearFeatures
from django.contrib.auth import get_user_model

User = get_user_model()


class ApiAppResource(resources.ModelResource):
    class Meta:
        model = LinearFeatures
        import_id_fields = ['id']

