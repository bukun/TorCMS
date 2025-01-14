import requests
import json
from place.geofea.models  import PlanarFeatures
from rest_framework import generics
from rest_framework import permissions
from .serializers import ApiAppSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
from django_filters import rest_framework
from django.http import HttpResponse
from django.shortcuts import render

User = get_user_model()
from django.http import JsonResponse
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance


class DataList(generics.ListCreateAPIView):
    queryset = PlanarFeatures.objects.all()
    serializer_class = ApiAppSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = ['location_name', ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DataDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PlanarFeatures.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


def ajax_load_cities(request, region):
    if request.method == 'GET':
        user = request.user  # 获取用户
        # user.get_group_permissions()

        reg_rec = PlanarFeatures.objects.filter(region=region)
        dict_list = [instance.to_dict() for instance in reg_rec]
        my_json = json.dumps(dict_list, ensure_ascii=False)
        return JsonResponse(my_json, safe=False)


def map_view(request):
    region_recs = PlanarFeatures.objects.values_list('region', flat=True).distinct()

    region_list = list(set(region_recs))

    data_recs = []
    for region in region_list:
        reg_rec = PlanarFeatures.objects.filter(region=region)
        data_recs.append({region: reg_rec})

    context = {'region_data': data_recs}

    return render(request, 'planar_features/map_view.html', context)


def get_city(request, lat, lng):
    # 创建一个地理空间点对象

    coordinates = Point(float(lng), float(lat), srid=4326)

    # 获取距离这个坐标最近的城市
    closest_city = PlanarFeatures.objects.annotate(
        distance=Distance('location', coordinates)
    ).order_by('distance').first()
    # 输出城市名
    print(f"The closest city is: {closest_city.location_name}")
    my_json = json.dumps(closest_city.location_name, ensure_ascii=False)
    return JsonResponse(my_json, safe=False)


def get_by_id(request, id):
    reg_rec = PlanarFeatures.objects.filter(id=id)
    dict_list = [instance.to_dict() for instance in reg_rec]
    my_json = json.dumps(dict_list, ensure_ascii=False)

    return JsonResponse(my_json, safe=False)
