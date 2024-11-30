from import_export import resources

from .models import ThePage
from django.contrib.auth import get_user_model

User = get_user_model()


class PageResource(resources.ModelResource):
    class Meta:
        model = ThePage
        import_id_fields = ['title']

