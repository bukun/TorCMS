from qgis.qgis_map.models import BigScreenMapCategory
from rest_framework import generics
from rest_framework import permissions
from .serializers import BigScreenMapCategorySerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
from django_filters import rest_framework
from django.views.generic import ListView
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.aggregates import Count
from django.contrib.sites.models import Site
from base.models import get_template,get_paginator

parent_template = get_template()
current_site = Site.objects.get_current()
User = get_user_model()


class BigScreenMapCategoryList(generics.ListCreateAPIView):
    queryset = BigScreenMapCategory.objects.filter(sites__id=current_site.id)
    serializer_class = BigScreenMapCategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = ['name', ]

    # 将request.user与author绑定
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BigScreenMapCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BigScreenMapCategory.objects.filter(sites__id=current_site.id)
    serializer_class = BigScreenMapCategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class BigScreenMapCategoryListView(ListView):
    model = BigScreenMapCategory
    context_object_name = 'Category'


def BigScreenMapCategoryIndex(request, pk):
    all_cat = BigScreenMapCategory.objects.filter(sites__id=current_site.id).order_by('-create_time')
    context = {'Category': all_cat,'parent_template': parent_template}
    return render(request, 'bigscreen_map_category/category_index.html', context)


def BigScreenMapCategoryDataList(request, pk):
    category_rec = get_object_or_404(BigScreenMapCategory, pk=pk)
    all_cat = BigScreenMapCategory.objects.filter(sites__id=current_site.id).order_by('-create_time')
    data_recs = category_rec.bigscreendata.filter(sites__id=current_site.id)
    is_paginated, page_obj = get_paginator(data_recs, request)

    context = {'data': page_obj, 'cat_name': category_rec.name, 'is_paginated': is_paginated, 'Category': all_cat,'parent_template': parent_template}
    return render(request, 'bigscreen_map_category/data_list.html', context)
def index(request):
    category_rec = BigScreenMapCategory.objects.filter(sites__id=current_site.id).order_by('-create_time')
    cat_rec = []
    for cat in category_rec:
        data = cat.zhongmengdata.filter(sites__id=current_site.id)[:4]

        cat_rec.append({'cat_id':cat.id,'cat_name': cat.name, 'data': data})
    context = {'cat_data': cat_rec,'parent_template': parent_template}

    return render(request, 'bigscreen_map_category/index.html', context)