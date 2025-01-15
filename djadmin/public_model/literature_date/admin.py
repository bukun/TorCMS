from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from public_model.literature_author.models import LiteratureDate
from .resources import CategoryResource
from mptt.admin import MPTTModelAdmin
from django.db.models.aggregates import Count


class LiteratureDateAdmin(ImportExportModelAdmin):
    resource_class = CategoryResource
    # 控制哪些字段会显示在Admin 的修改列表页面中
    list_display = ("id","pub_date", "order",)


    list_per_page = 20
    filter_horizontal = ('sites',)



# 注册app的admin
admin.site.register(LiteratureDate, LiteratureDateAdmin)
