from import_export import resources

from .models import CrawlDocumentEN,RzLog
from django.contrib.auth import get_user_model

User = get_user_model()


class DataResource(resources.ModelResource):
    class Meta:
        model = CrawlDocumentEN
        import_id_fields = ['id']

class RZLogResource(resources.ModelResource):
    class Meta:
        model = RzLog
        import_id_fields = ['id']
