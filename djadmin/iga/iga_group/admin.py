from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import iga_group
from .resources import IgagroupResource
from django.db import models
from django.forms import TextInput, Textarea
from django.db.models.aggregates import Count

class igagroupadmin(ImportExportModelAdmin):
    resource_class = IgagroupResource
    # 控制哪些字段会显示在Admin 的修改列表页面中
    list_display = ("id","title","get_count")
    list_per_page = 20
    search_fields = ('title',)
    def get_count(self, obj):
        rec = iga_group.objects.annotate(num_posts=Count('iga_room')).filter(title=obj.title)

        return rec[0].num_posts

    get_count.short_description = '数量'
    get_count.admin_order_field = 'get_count'
# 注册app的admin
admin.site.register(iga_group, igagroupadmin)
