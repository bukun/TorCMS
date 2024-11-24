import json
import requests
import logging
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import XZQH
from .resources import ApiAppResource
from django.db import models
from django.forms import TextInput, Textarea
from mptt.admin import MPTTModelAdmin
logger = logging.getLogger(__name__)


class XZQHAdmin(MPTTModelAdmin,ImportExportModelAdmin):
    resource_class = ApiAppResource
    # 控制哪些字段会显示在Admin 的修改列表页面中
    list_display = ("zoning","name", "content")
    # 用来排序
    list_display_links = ("zoning","name")

    list_per_page = 100

    search_fields = ("zoning","name", "content")

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'style': 'width: 80%;'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 6, 'style': 'width: 80%;'})},
    }




# 注册app的admin
admin.site.register(XZQH, XZQHAdmin)
