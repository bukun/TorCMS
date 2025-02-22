import json

from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.shortcuts import get_object_or_404, redirect, render
from django_filters import rest_framework
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from qgis.qgis_map.models import *

from .permissions import IsOwnerOrReadOnly
from .serializers import vectorlayerSerializer

current_site = Site.objects.get_current()
User = get_user_model()


class vectorlayerList(generics.ListCreateAPIView):
    queryset = vectorlayer.objects.filter(sites__id=current_site.id)
    serializer_class = vectorlayerSerializer
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


class vectorlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = vectorlayer.objects.filter(sites__id=current_site.id)
    serializer_class = vectorlayerSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class LabelAPIView(APIView):
    def get(self, request, pk):
        obj = QgisLabel.objects.get(name=pk)
        res = obj.vectorlayer.all()
        maplist = []
        for x in res:
            if x not in maplist:
                maplist.append(vectorlayerSerializer(x).data)
        return Response({'result': maplist})


def vectorlayerDetailView(request, mapid, category):
    # 从url里获取单个任务的pk值，然后查询数据库获得单个对象
    data = get_object_or_404(vectorlayer, pk=mapid)
    if category == 'bigscreen':
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
