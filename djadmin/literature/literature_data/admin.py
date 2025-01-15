from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from ..literature_category.models import Literature
from .resources import literatureResource
from django.db import models
from django.forms import TextInput, Textarea

class LiteratureAdmin(ImportExportModelAdmin):
    resource_class = literatureResource
    # 控制哪些字段会显示在Admin 的修改列表页面中
    list_display = (
        "id","title","category", "theme", "type",  "create_time","update_time",)
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'style': 'width: 80%;'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 6, 'style': 'width: 80%;'})},
    }
    # 用来排序
    ordering = ["create_time","category", "theme", "update_time"]
    list_per_page = 20
    filter_horizontal = ('label','sites',"author",)
    search_fields = ('title', 'cnt_md','theme','type')



    def save_model(self, request, obj, form, change):
        obj.user = request.user

        super().save_model(request, obj, form, change)
# 注册app的admin
admin.site.register(Literature, LiteratureAdmin)
