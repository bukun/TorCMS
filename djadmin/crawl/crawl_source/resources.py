from import_export import resources

from .models import CrawlSource
from django.contrib.auth import get_user_model

User = get_user_model()


class CrawlSourceResource(resources.ModelResource):
    class Meta:
        model = CrawlSource
        import_id_fields = ['title']

