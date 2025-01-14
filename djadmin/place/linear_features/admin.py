import json
import requests
import logging
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from place.geofea.models  import LinearFeatures
from .resources import ApiAppResource
from django.db import models
from django.forms import TextInput, Textarea

logger = logging.getLogger(__name__)
from leaflet.admin import LeafletGeoAdmin


class LinearFeaturesAdmin(LeafletGeoAdmin, ImportExportModelAdmin):
    resource_class = ApiAppResource
    # 控制哪些字段会显示在Admin 的修改列表页面中
    list_display = ("id","region","location_name", "historical_name", "set_time", "cancel_time", "lat", "lon", "content","zoom")
    # 用来排序
    list_display_links = ("location_name",)

    list_per_page = 20
    list_filter = ("is_en", "region", "location_name",)
    search_fields = ('location_name', 'historical_name', 'set_time', 'cancel_time', 'content','region')

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'style': 'width: 80%;'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 6, 'style': 'width: 80%;'})},
    }

    def save_model(self, request, obj, form, change):
        obj.update_user = request.user
        obj.receiver = request.user.username

        # 用于记录数据变化信息
        if form.has_changed():
            change_list = form.changed_data

            try:
                changed_dict = form.cleaned_data

                for i in change_list:
                    if i == 'location':
                        loc = changed_dict[i]  # 当前新写入的数据

                        obj.lat = loc.y
                        obj.lon = loc.x

            except  BaseException as e:
                logger.error(f'错误类型是:{e.__class__.__name__}\n错误原因: {e}')


        super().save_model(request, obj, form, change)


# 注册app的admin
admin.site.register(LinearFeatures, LinearFeaturesAdmin)
