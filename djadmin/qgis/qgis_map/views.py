import json

from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.shortcuts import get_object_or_404, redirect, render
from django_filters import rest_framework
from rest_framework import generics, permissions
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from base.models import get_template

from .models import QgisLabel, qgismap
from .permissions import IsOwnerOrReadOnly
from .serializers import QgisMapSerializer

parent_template = get_template()
current_site = Site.objects.get_current()
User = get_user_model()


class QgisMapList(generics.ListCreateAPIView):
    queryset = qgismap.objects.filter(sites__id=current_site.id)
    serializer_class = QgisMapSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = [
        'title',
        'mapid',
        'zhongbacategory',
        'yaoucategory',
        'zhongmengcategory',
        'heitucategory',
        'ansocategory',
        'bigscreencategory',
        'label',
    ]

    # 将request.user与author绑定
    def perform_create(self, serializer):
        serializer.save(user_name=self.request.user)


class QgisMapDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = qgismap.objects.filter(sites__id=current_site.id)
    serializer_class = QgisMapSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class LabelAPIView(APIView):
    def get(self, request, pk):
        obj = QgisLabel.objects.get(name=pk)
        res = obj.qgismap.all()
        maplist = []
        for x in res:
            if x not in maplist:
                maplist.append(QgisMapSerializer(x).data)
        return Response({'result': maplist})


def QgisMapDetailView(request, mapid, category):
    # 从url里获取单个任务的pk值，然后查询数据库获得单个对象
    data = get_object_or_404(qgismap, pk=mapid)
    if category == 'anso':
        data_cat = ANSOMapCategory.objects.filter(sites__id=current_site.id)
    elif category == 'yaou':
        data_cat = yaoumapcategory.objects.filter(sites__id=current_site.id)
    elif category == 'zhongba':
        data_cat = zhongbamapcategory.objects.filter(sites__id=current_site.id)
    elif category == 'zhongmeng':
        data_cat = zhongmengmapcategory.objects.filter(
            sites__id=current_site.id
        ).order_by('-create_time')
    elif category == 'heitu':
        data_cat = heitumapcategory.objects.filter(sites__id=current_site.id)
    elif category == 'bigscreen':
        data_cat = BigScreenMapCategory.objects.filter(sites__id=current_site.id)

    else:
        data_cat = yaoumapcategory.objects.filter(sites__id=current_site.id)

    return render(
        request,
        "qgis_map/data_detail.html",
        {
            "data": data,
            "Category": data_cat,
            "cat_name": category,
            "parent_template": f'{category}_base.html',
        },
    )


# todo 暂时允许所有人获取 以后根据要求再改
@permission_classes((AllowAny,))
class APIGetHeituMapList(APIView):
    # 根据 黑土的分类 获取 黑土所有图层列表
    # 如果写了需要的分类列表，就返回分类的列表，如果没有，就返回所有黑土分类的列表
    def get(self, request):
        data_cat = heitumapcategory.objects.all()

        heitu_category_string = self.request.query_params.get(
            'heitu_category_list', None
        )

        map_list = {}

        if heitu_category_string != None:
            heitu_category_list = json.loads(heitu_category_string)
            for cat in heitu_category_list:
                one_list = []

                get_cat_id = heitumapcategory.objects.filter(name=cat)
                queryset = qgismap.objects.filter(heitucategory=get_cat_id.all()[0].id)

                for j in queryset.all():
                    one_data = QgisMapSerializer(j)

                    one_list.append(one_data.data)

                map_list[cat] = one_list

        else:
            for i in data_cat:
                one_list = []
                queryset = qgismap.objects.filter(heitucategory=i.id)

                for j in queryset.all():
                    one_data = QgisMapSerializer(j)

                    one_list.append(one_data.data)

                map_list[i.name] = one_list

        return Response({'msg': map_list, 'code': 200})
