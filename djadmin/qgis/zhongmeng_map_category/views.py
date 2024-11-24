from .models import zhongmengmapcategory
from rest_framework import generics
from rest_framework import permissions
from .serializers import ZhongmengMapCategorySerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
from django_filters import rest_framework
from django.views.generic import ListView
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.aggregates import Count
from django.contrib.sites.models import Site
from base.models import get_template

parent_template = get_template()
current_site = Site.objects.get_current()
User = get_user_model()


class ZhongmengMapCategoryList(generics.ListCreateAPIView):
    queryset = zhongmengmapcategory.objects.filter(sites__id=current_site.id)
    serializer_class = ZhongmengMapCategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = ['name', ]

    # 将request.user与author绑定
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ZhongmengMapCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = zhongmengmapcategory.objects.filter(sites__id=current_site.id)
    serializer_class = ZhongmengMapCategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class ZhongmengMapCategoryListView(ListView):
    model = zhongmengmapcategory
    context_object_name = 'Category'


def ZhongmengMapCategoryIndex(request, pk):
    all_cat = zhongmengmapcategory.objects.filter(sites__id=current_site.id).order_by('-create_time')
    context = {'Category': all_cat,'parent_template': parent_template}
    return render(request, 'zhongmeng_map_category/category_index.html', context)


def ZhongmengMapCategoryDataList(request, pk):
    category_rec = get_object_or_404(zhongmengmapcategory, pk=pk)
    all_cat = zhongmengmapcategory.objects.filter(sites__id=current_site.id).order_by('-create_time')
    data_recs = category_rec.zhongmengdata.filter(sites__id=current_site.id)
    paginator = Paginator(data_recs, 20)  # 实例化一个分页对象, 每页显示10个
    page = request.GET.get('page')  # 从URL通过get页码，如?page=3
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)  # 如果传入page参数不是整数，默认第一页
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    is_paginated = True if paginator.num_pages > 1 else False  # 如果页数小于1不使用分页

    context = {'data': page_obj, 'cat_name': category_rec.name, 'is_paginated': is_paginated, 'Category': all_cat,'parent_template': parent_template}
    return render(request, 'zhongmeng_map_category/data_list.html', context)
def index(request):
    category_rec = zhongmengmapcategory.objects.filter(sites__id=current_site.id).order_by('-create_time')
    cat_rec = []
    for cat in category_rec:
        data = cat.zhongmengdata.filter(sites__id=current_site.id)[:4]

        cat_rec.append({'cat_id':cat.id,'cat_name': cat.name, 'data': data})
    context = {'cat_data': cat_rec,'parent_template': parent_template}

    return render(request, 'zhongmeng_map_category/index.html', context)