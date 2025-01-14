from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from post.doc_category.models import Topic,Comment
from .resources import TopicResource,CommentResource
from mptt.admin import MPTTModelAdmin
from django.db import models
from django.forms import TextInput, Textarea
class TopictAdmin(ImportExportModelAdmin):
    resource_class = TopicResource
    # 控制哪些字段会显示在Admin 的修改列表页面中
    list_display = ("id","title", "user",  "create_time","update_time")

    # 用来排序
    ordering = ["create_time", ]
    list_per_page = 20

    search_fields = ('title', 'cnt_md')

    filter_horizontal = ('label','sites')
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'style': 'width: 80%;'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 6, 'style': 'width: 80%;'})},
    }

admin.site.register(Topic, TopictAdmin)

class CommentAdmin(MPTTModelAdmin,ImportExportModelAdmin):
    resource_class = CommentResource
    # 控制哪些字段会显示在Admin 的修改列表页面中
    list_display = ("content", "user",  "create_time")
    # 用来排序
    ordering = ["create_time", ]
    list_per_page = 20

    search_fields = ('content', 'user')



admin.site.register(Comment, CommentAdmin)

