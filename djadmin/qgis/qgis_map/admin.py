from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import qgismap
from .resources import QgisMapResource
from django.contrib import admin

from django.db import models
from django.forms import TextInput, Textarea

class qgismapadmin(ImportExportModelAdmin):
    resource_class = QgisMapResource
    # 控制哪些字段会显示在Admin 的修改列表页面中
    list_display = (
        "id","mapid","title", "create_time","update_time","zhongbacategory","yaoucategory",
        "zhongmengcategory","heitucategory","ansocategory","bigscreencategory")
    ordering = [ "create_time", "update_time", ]
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'style': 'width: 80%;'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 6, 'style': 'width: 80%;'})},
    }
    list_per_page = 20

    search_fields = ('title', 'mapid','id')
    list_display_links = ("title",)
    filter_horizontal = ('label','sites',"bigscreencategory")
    list_filter = ("zhongbacategory","yaoucategory","zhongmengcategory","heitucategory","ansocategory","bigscreencategory")
    # filter_horizontal = ('label',)
    # def get_category(self, obj):
    #     rec = Category.objects.get(id__exact=obj.category)
    #     return rec.name
    #
    # get_category.short_description = '分类名称'
    # get_category.admin_order_field = 'get_category'

# 注册app的admin
admin.site.register(qgismap, qgismapadmin)
