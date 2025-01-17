import json
import os
import openpyxl
from .models import iga_group
from .models import iga_floor
from rest_framework import generics
from rest_framework import permissions
from .serializers import IgagroupSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
from django_filters import rest_framework
from django.views.generic import DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sites.models import Site
from django.http import HttpResponse
from base.models import get_template,get_paginator
from django.conf import settings
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.forms.models import model_to_dict

parent_template = get_template()
current_site = Site.objects.get_current()
User = get_user_model()


class DataList(generics.ListCreateAPIView):
    queryset = iga_group.objects.filter(sites__id=current_site.id)
    serializer_class = IgagroupSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = ['title']

    # 将request.user与author绑定
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DataDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = iga_group.objects.filter(sites__id=current_site.id)
    serializer_class = IgagroupSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

def IgaIndex(request):
    # i = 0
    groups_rec = iga_group.objects.all().order_by('id')
    group_rec = []
    for group in groups_rec:
        data = group.iga_room.all()
        area_count = 0.0
        if data:
            for dat in data:
                # if dat.areaf != '无面积信息':
                area_count = area_count + dat.areafloat
                # print(area_count)
            group_rec.append({'group_id': group.id, 'group_title': group.title, 'data': data,'count':data.count(),'area_count':area_count})
            # i= i + data.count()
    # print(i)
    context = {'cat_data': group_rec, 'parent_template': parent_template}

    return render(request, 'groups/groups.html', context)

def IgagroupDataList(request, pk):
    category_rec = get_object_or_404(iga_group, pk=pk)
    all_cat = iga_group.objects.all()
    data_recs = category_rec.iga_room.all().order_by('num')
    dict_instances = [instance.floor_num for instance in data_recs]
    num_instances = [instance.num for instance in data_recs]

    paginator = Paginator(data_recs, 20)  # 实例化一个分页对象, 每页显示10个
    is_paginated, page_obj = get_paginator(data_recs, request)
    context = {'data': page_obj,'data_json':dict_instances, 'data_num':num_instances,'cat_name': category_rec.title,
               'is_paginated': is_paginated, 'Category': all_cat, 'parent_template': parent_template
               }
    return render(request, 'groups/data_list.html', context)
def ajax_update_info(request):
    if request.method == 'GET':
        groupid = request.GET.get('groupid', '1')  # 从GET请求中获取参数


        cat = iga_group.objects.filter(id=groupid).first()
        data_recs = cat.iga_room.all().order_by('num')
        data_list =[]
        for info in data_recs:
            dic = {}
            dic['building'] = info.building
            dic['floor'] = iga_floor.objects.filter(num=info.floor).first().num
            dic['num'] = info.num
            dic['title'] = info.get_title_display()
            dic['areafloat'] = info.areafloat
            dic['staff'] = info.staff
            if dic not in data_list:data_list.append(dic)
        dict_instances = [instance.floor_num for instance in data_recs]
        context = {'title': cat.title,'data_json':dict_instances,'data_list':data_list}
        # print(context)
        return JsonResponse(context)
    else:
        return JsonResponse({'message': 'fail'})