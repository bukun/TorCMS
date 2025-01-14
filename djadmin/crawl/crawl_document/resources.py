from import_export import resources

from ..crawl_source.models import CrawlDocument
from django.contrib.auth import get_user_model

User = get_user_model()


class DataResource(resources.ModelResource):
    class Meta:
        model = CrawlDocument
        import_id_fields = ['id']

