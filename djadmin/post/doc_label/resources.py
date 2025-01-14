from import_export import resources

from post.doc_category.models import DocLabel
from django.contrib.auth import get_user_model

User = get_user_model()


class LabelResource(resources.ModelResource):
    class Meta:
        model = DocLabel
        import_id_fields = ['name']

