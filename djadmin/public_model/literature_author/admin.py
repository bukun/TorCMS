from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import LiteratureAuthor
from .resources import CategoryResource
from mptt.admin import MPTTModelAdmin
from django.db.models.aggregates import Count


class LiteratureAuthorAdmin(ImportExportModelAdmin):
    resource_class = CategoryResource
    # 控制哪些字段会显示在Admin 的修改列表页面中
    list_display = ("name", "order", )


    list_per_page = 20
    filter_horizontal = ('sites',)



# 注册app的admin
admin.site.register(LiteratureAuthor, LiteratureAuthorAdmin)
