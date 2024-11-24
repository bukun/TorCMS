"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import json
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from django.views.generic import TemplateView


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from post.document import views as doc_views
from qgis.yaou_map_category import views as yaouview
from qgis.anso_map_category import views as ansoview
from zhongnan.zn_dataset_category import views as znview
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

@login_required()
def userdata(request):
    print("=" * 80)

    user = request.user
    info = {"username": user.username}

    print("*" * 50)
    print("")
    print(info)
    return HttpResponse(json.dumps(info), content_type="application/json")


urlpatterns = [

    path('wagtail_cms/', include(wagtailadmin_urls)),  # 管理中心
    path('wagtail_documents/', include(wagtaildocs_urls)),  # 文件
    path('wagtail_pages/', include(wagtail_urls)),  # 知识页面


    path('static-docs/', TemplateView.as_view(template_name='index.html')),
    # path('', cat_views.Categorylist, name='category_index'),
    path('doc_save/', doc_views.save_doc, name='doc_spider_save'),
    # path('', yaouview.index, name='sindex'),
    path('', yaouview.yaou_index, name='yaou_index'),
    path('zn/', znview.index, name='zn_dataset_index'),

    # path('', ansoview.index, name='anso_index'),

    path('admin/', admin.site.urls),
    # path('api-auth/', include('rest_framework.urls')), # 用户登录页面
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('ckeditor/', include('ckeditor_uploader.urls')),

    path('users/', include('users.urls')),  # 后台用户管理
    # path('groups/', include('groups.urls')),  # 后台用户管理

    path('categorys/', include('data.categorys.urls')),  # 分类管理
    path('labels/', include('data.labels.urls')),  # 标签管理
    path('dataset/', include('data.dataset.urls')),  # 数据管理

    path('map/', include('data.map.urls')),  # 地图

    path('world/', include('world.urls')),

    path('igais_category/', include('igais.igais_category.urls')),  # igais分类
    path('igais_data/', include('igais.igais_data.urls')),  # igais数据
    path('igais_label/', include('igais.igais_label.urls')),  # igais标签

    path('qgis_map/', include('qgis.qgis_map.urls')),  #
    path('heitu_map_category/', include('qgis.heitu_map_category.urls')),  #
    path('zhongmeng_map_category/', include('qgis.zhongmeng_map_category.urls')),  #
    path('yaou_map_category/', include('qgis.yaou_map_category.urls')),  #
    path('portal/', include('qgis.yaou_map_category.urls')),  #
    path('zhongba_map_category/', include('qgis.zhongba_map_category.urls')),  #
    path('anso_map_category/', include('qgis.anso_map_category.urls')),  #
    path('bigscreen_map_category/', include('qgis.bigscreen_map_category.urls')),  #
    path('qgis_label/', include('qgis.qgis_label.urls')),  #
    path('vector_layer/', include('qgis.vector_layer.urls')),  #矢量图层

    # path('farmpro/', include('heitu_granary.farmpro.urls')),  # 农产品最新价格
    # path('farmpro_avg/', include('heitu_granary.farmpro_avg.urls')),  # 农产品地区均价

    path('doc_category/', include('post.doc_category.urls')),  # 普通文档分类，
    path('doc_label/', include('post.doc_label.urls')),  # 普通文档标签，
    path('document/', include('post.document.urls')),  # 普通文档，
    path('topic/', include('post.topic.urls')),  # 协同计算？问答

    path('page/', include('pages.page.urls')),

    path('apiapp/', include('apiapp.urls')),  # app，

    path('crawl_source/', include('crawl.crawl_source.urls')),  # 爬取的数据来源，
    path('crawl_label/', include('crawl.crawl_label.urls')),  # 爬取的数据标签，
    path('crawl_document/', include('crawl.crawl_document.urls')),  # 爬取的中文数据
    path('crawl_document_en/', include('crawl.crawl_document_en.urls')),  # 爬取的英文数据

    path('ckeditor/', include('ckeditor_uploader.urls')),  # ckckeditor图片上传
    path('mdeditor/', include('mdeditor.urls')),  # ckckeditor图片上传



    # 专题资源管理
    path('resource_category/', include('dresource.resource_category.urls')),  # 分类管理
    path('resource_label/', include('dresource.resource_label.urls')),  # 标签管理
    path('resource/', include('dresource.resource_dataset.urls')),  # 数据管理

    # 翻译库管理
    path('trans_en_zh/', include('translation_library.trans_en_zh.urls')),  # 英-中翻译管理
    path('trans_zh_en/', include('translation_library.trans_zh_en.urls')),  # 中-英翻译管理

    # 地名库
    path('place_name/', include('place.place_name.urls')),  # 地名库
    path('linear_features/', include('place.linear_features.urls')),  # 线状要素库
    path('planar_features/', include('place.planar_features.urls')),  # 面状要素库

    # http://geofea.gislab.cn/#/html/index/
    path('geofea/', include('place.geofea.urls')),
    path('thematic_maps/', include('place.thematic_maps.urls')),
    path('test_text/', include('place.test_text.urls')),
    path('geopage/', include('place.geopage.urls')),
    path('xzqh/', include('place.xzqh.urls')),

    # 长春工程建设管理
    path('changchun_project/', include('changchun_project.urls')),

    path('users/', include('users.urls')),  # 后台用户管理
    # path('groups/', include('groups.urls')),  # 后台用户管理

    path('categorys/', include('data.categorys.urls')),  # 分类管理
    path('labels/', include('data.labels.urls')),  # 标签管理
    path('dataset/', include('data.dataset.urls')),  # 数据管理
    path('map/', include('data.map.urls')),  # 地图

    path('zn_dataset/', include('zhongnan.zn_dataset.urls')),  # 中南数据管理
    path('zn_dcat/', include('zhongnan.zn_dataset_category.urls')),  # 中南数据分类管理
    path('zn_dlabel/', include('zhongnan.zn_dataset_label.urls')),  # 中南数据标签管理
    path('zn_event/', include('zhongnan.zn_event.urls')),  # 中南事件管理
    path('zn_ecat/', include('zhongnan.zn_event_category.urls')),  # 中南事件分类管理
    path('zn_elabel/', include('zhongnan.zn_event_label.urls')),  # 中南事件标签管理

    path('barn_dataset/', include('heitu_barn.barn_dataset.urls')),  # 黑土粮仓农业站数据
    path('barn_device/', include('heitu_barn.barn_device.urls')),  # 黑土粮仓农业站数据
    path('barn_field/', include('heitu_barn.barn_field.urls')),  # 黑土粮仓农业站数据

    path('device_soilmoisture/', include('heitu_barn.device_soilmoisture.urls')),  # 黑土粮仓农业气象站数据
    path('device_soilfiveparameters/', include('heitu_barn.device_soilfiveparameters.urls')),  # 黑土粮仓农业气象站数据
    path('device_soilfiveparametersv2/', include('heitu_barn.device_soilfiveparametersv2.urls')),  # 黑土粮仓农业气象站数据
    path('device_meteorology/', include('heitu_barn.device_meteorology.urls')),  # 黑土粮仓农业气象站数据

    path('lgeojson/', include('layerstyle.lgeojson.urls')),  # 在线制图数据管理 GeoJSON地理数据
    path('lprogram/', include('layerstyle.lprogram.urls')),  # 在线制图数据管理 项目管理

    path('literature/', include('literature.literature_data.urls')),  # 文献管理
    path('literature_category/', include('literature.literature_category.urls')),  # 文献分类管理
    path('literature_label/', include('literature.literature_label.urls')),  # 文献标签管理
    path('jupyter_data/', include('jupyters.jupyter_data.urls')),  # 科学计算模型数据
    path('jupyter_category/', include('jupyters.jupyter_category.urls')),  # 科学计算模型分类

    path("o/", include("oauth2_provider.urls", namespace="oauth2_provider")),
    path("userdata", userdata, name="userdata"),
    path('friendship/', include('friendship.urls')),
    path('bigscreen/', include('bigscreen.bigscreen_data.urls')), #大屏数据
    path('jump_btn/', include('bigscreen.jump_btn.urls')), #大屏数据

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
