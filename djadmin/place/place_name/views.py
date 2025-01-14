import requests
import json
from place.geofea.models  import PlaceName
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
    queryset = PlaceName.objects.all()
    serializer_class = ApiAppSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = ['location_name', ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DataDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PlaceName.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


def ajax_load_cities(request, region):
    if request.method == 'GET':
        user = request.user  # 获取用户
        # user.get_group_permissions()

        reg_rec = PlaceName.objects.filter(region=region)
        dict_list = [instance.to_dict() for instance in reg_rec]
        my_json = json.dumps(dict_list, ensure_ascii=False)
        return JsonResponse(my_json, safe=False)


def map_view(request):
    region_recs = PlaceName.objects.values_list('region', flat=True).distinct()

    region_list = list(set(region_recs))

    data_recs = []
    for region in region_list:
        reg_rec = PlaceName.objects.filter(region=region)
        data_recs.append({region: reg_rec})

    context = {'region_data': data_recs}

    return render(request, 'place_name/map_view.html', context)


def get_city(request, lng, lat ):
    # 创建一个地理空间点对象

    print('=' * 40)
    print(lng, lat)

    # ToDo: 反了
    # coordinates = Point(float(lng), float(lat), srid=4326)
    coordinates = Point(float(lat), float(lng), srid=4326)



    print(coordinates)

    # 获取距离这个坐标最近的城市
    closest_city = PlaceName.objects.annotate(
        distance=Distance('location', coordinates)
        ).order_by('distance')[:10]
    # 输出城市名
    # print(f"The closest city is: {closest_city.location_name}")
    out_dict = {}
    idx = 1
    for the_city in closest_city:
        out_dict[idx] = [the_city.location_name,  the_city.lon, the_city.lat]
        idx = idx + 1
    my_json = json.dumps(out_dict, ensure_ascii=False)
    return JsonResponse(my_json, safe=False)


def get_by_id(request, id):
    reg_rec = PlaceName.objects.filter(id=id)
    dict_list = [instance.to_dict() for instance in reg_rec]
    my_json = json.dumps(dict_list, ensure_ascii=False)

    return JsonResponse(my_json, safe=False)
