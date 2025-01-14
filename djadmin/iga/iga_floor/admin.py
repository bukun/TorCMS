from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from iga.iga_group.models import iga_floor
from .resources import IgafloorResource
from django.db import models
from django.forms import TextInput, Textarea
from django.db.models.aggregates import Count

class igaflooradmin(ImportExportModelAdmin):
    resource_class = IgafloorResource
    # 控制哪些字段会显示在Admin 的修改列表页面中
    list_display = ("id","num","get_count")
    list_per_page = 20
    search_fields = ('num',)
    def get_count(self, obj):
        rec = iga_floor.objects.annotate(num_posts=Count('iga_room')).filter(num=obj.num)

        return rec[0].num_posts

    get_count.short_description = '数量'
    get_count.admin_order_field = 'get_count'


# 注册app的admin
admin.site.register(iga_floor, igaflooradmin)
