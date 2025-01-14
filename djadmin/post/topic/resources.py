from import_export import resources

from post.doc_category.models import Topic,Comment
from django.contrib.auth import get_user_model

User = get_user_model()


class TopicResource(resources.ModelResource):
    class Meta:
        model = Topic
        import_id_fields = ['id']

class CommentResource(resources.ModelResource):
    class Meta:
        model = Comment
        import_id_fields = ['id']
