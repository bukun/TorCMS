import logging
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Barndataset
from .resources import BarndatasetResource
from django.db import models
from django.forms import TextInput, Textarea
logger = logging.getLogger(__name__)

from leaflet.admin import LeafletGeoAdmin
# 设置默认的经纬度为长春市的大致中心点（纬度，经度）
DEFAULT_LOCATION = (43.88, 125.35)


class barndatasetadmin(LeafletGeoAdmin,ImportExportModelAdmin):
    resource_class = BarndatasetResource
    # 控制哪些字段会显示在Admin 的修改列表页面中
    list_display = (
        "title","lat", "lon", "create_time","update_time",)
    default_zoom = 5  # 设置默认的缩放级别
    default_location = DEFAULT_LOCATION  # 设置默认显示的经纬度
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'style': 'width: 80%;'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 6, 'style': 'width: 80%;'})},
    }
    # 用来排序
    ordering = ["create_time",]
    list_per_page = 20

    search_fields = ('name',"deviceid",'cnt_md')

    # filter_horizontal = ('label',)
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
    # def save_model(self, request, obj, form, change):
    #     obj.user = request.user
    #
    #     super().save_model(request, obj, form, change)
# 注册app的admin
admin.site.register(Barndataset, barndatasetadmin)
