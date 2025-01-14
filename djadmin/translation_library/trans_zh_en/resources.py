from import_export import resources

from translation_library.trans_en_zh.models  import TranslationZHEN
from django.contrib.auth import get_user_model

User = get_user_model()


class ApiAppResource(resources.ModelResource):
    class Meta:
        model = TranslationZHEN
        import_id_fields = ['id']

