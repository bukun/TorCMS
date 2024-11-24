from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Page
from .resources import PageResource
from django.db.models.aggregates import Count
from django.db import models
from django.forms import TextInput, Textarea


class PageAdmin(ImportExportModelAdmin):
    resource_class = PageResource
    # 控制哪些字段会显示在Admin 的修改列表页面中
    list_display = ("id", "slug", "title",)
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'style': 'width: 80%;'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 6, 'style': 'width: 80%;'})},
    }

    list_per_page = 20
    filter_horizontal = ('sites',)
    def save_model(self, request, obj, form, change):
        obj.user = request.user

        super().save_model(request, obj, form, change)


# 注册app的admin
admin.site.register(Page, PageAdmin)
