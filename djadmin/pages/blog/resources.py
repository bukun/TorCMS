from import_export import resources

from .models import Page
from django.contrib.auth import get_user_model

User = get_user_model()


class PageResource(resources.ModelResource):
    class Meta:
        model = Page
        import_id_fields = ['title']

