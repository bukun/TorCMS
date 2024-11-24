from import_export import resources

from .models import CrawlLabel
from django.contrib.auth import get_user_model

User = get_user_model()


class LabelResource(resources.ModelResource):
    class Meta:
        model = CrawlLabel
        import_id_fields = ['name']

