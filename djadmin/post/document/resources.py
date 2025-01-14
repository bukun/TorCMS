from import_export import resources

from post.doc_category.models import Document
from django.contrib.auth import get_user_model

User = get_user_model()


class DataResource(resources.ModelResource):
    class Meta:
        model = Document
        import_id_fields = ['id']

