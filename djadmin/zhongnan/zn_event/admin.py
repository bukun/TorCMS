from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from ..zn_event_category.models import ZNEvent
from .resources import DataResource
from django.db import models
from django.forms import TextInput, Textarea

class ZNEventadmin(ImportExportModelAdmin):
    resource_class = DataResource
    # 控制哪些字段会显示在Admin 的修改列表页面中
    list_display = (
        "id","title", "category", "user",  "create_time","update_time",)
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'style': 'width: 80%;'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 6, 'style': 'width: 80%;'})},
    }
    # 用来排序
    ordering = ["view_count", "create_time", "category", ]
    list_per_page = 20

    def get_readonly_fields(self, request, obj=None):

        return ['cnt_html']
    search_fields = ('title', 'cnt_md')

    filter_horizontal = ('label',)

    def save_model(self, request, obj, form, change):
        obj.user = request.user

        super().save_model(request, obj, form, change)
# 注册app的admin
admin.site.register(ZNEvent, ZNEventadmin)
