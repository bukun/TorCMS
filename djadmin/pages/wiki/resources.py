from import_export import resources
from pages.page.models import TheWiki
from django.contrib.auth import get_user_model

User = get_user_model()


class WikiResource(resources.ModelResource):
    class Meta:
        model = TheWiki
        import_id_fields = ['title']

