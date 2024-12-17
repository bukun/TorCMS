from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Jupyter
from .resources import JupyterResource
from django.db import models
from django.forms import TextInput, Textarea

class JupyterAdmin(ImportExportModelAdmin):
    resource_class = JupyterResource
    # 控制哪些字段会显示在Admin 的修改列表页面中
    list_display = (
       "id", "title", "file_id","dc_image","create_time","update_time")
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'style': 'width: 80%;'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 6, 'style': 'width: 80%;'})},
    }
    # fields = ['file', 'dc_image', 'logo']
    # 定义只读字段，这意味着它们在添加时不可编辑，但在更改时可编辑
    def get_readonly_fields(self, request, obj=None):
        if obj:  # obj为None时表示添加，非None时表示编辑
            pass
        else:
            return ['title','file_id','cnt_md','jupyter_port']
        return []
    # 用来排序
    ordering = ["create_time","dc_image","update_time"]

    list_per_page = 20

    search_fields = ('title', 'cnt_md','dc_image')
    filter_horizontal = ('shared_with','sites')
    # def save_model(self, request, obj, form, change):
    #
    #     obj.user = request.user
    #
    #     super().save_model(request, obj, form, change)
# 注册app的admin
admin.site.register(Jupyter, JupyterAdmin)
