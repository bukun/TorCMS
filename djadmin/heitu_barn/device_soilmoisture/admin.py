import logging
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Devicesoilmoisture
from .resources import DevicesoilmoistureResource
from django.db import models
from django.forms import TextInput, Textarea



class soilmoisturedadmin(ImportExportModelAdmin):
    resource_class = DevicesoilmoistureResource
    # 控制哪些字段会显示在Admin 的修改列表页面中
    list_display = (
        "devid","typenum","par_datetime",)


    # 用来排序
    ordering = ["create_time",]
    list_per_page = 20

    search_fields = ('devid',"typenum")

    def save_model(self, request, obj, form, change):
        obj.user = request.user

        super().save_model(request, obj, form, change)

admin.site.register(Devicesoilmoisture, soilmoisturedadmin)
