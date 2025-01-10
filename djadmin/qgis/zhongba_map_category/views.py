from .models import zhongbamapcategory
from rest_framework import generics
from rest_framework import permissions
from .serializers import ZhongbaMapCategorySerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
from django_filters import rest_framework
from django.views.generic import ListView
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.sites.models import Site
from base.models import get_template,get_paginator

parent_template = get_template()
current_site = Site.objects.get_current()
User = get_user_model()


class ZhongbaMapCategoryList(generics.ListCreateAPIView):
    queryset = zhongbamapcategory.objects.filter(sites__id=current_site.id)
    serializer_class = ZhongbaMapCategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = ['name',]

    # 将request.user与author绑定
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ZhongbaMapCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = zhongbamapcategory.objects.filter(sites__id=current_site.id)
    serializer_class = ZhongbaMapCategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class ZhongbaMapCategoryListView(ListView):
    model = zhongbamapcategory
    context_object_name = 'Category'


def ZhongbaMapCategoryIndex(request, pk):
    all_cat = zhongbamapcategory.objects.filter(sites__id=current_site.id)
    context = {'Category': all_cat,'parent_template': parent_template}
    return render(request, 'zhongba_map_category/category_index.html', context)


def ZhongbaMapCategoryDataList(request, pk):
    category_rec = get_object_or_404(zhongbamapcategory, pk=pk)
    all_cat = zhongbamapcategory.objects.filter(sites__id=current_site.id)
    data_recs = category_rec.zhongbadata.filter(sites__id=current_site.id)
    is_paginated, page_obj = get_paginator(data_recs, request)

    context = {'data': page_obj, 'cat_name': category_rec.name, 'is_paginated': is_paginated,'Category':all_cat,'parent_template': parent_template}
    return render(request, 'zhongba_map_category/data_list.html', context)
def index(request):
    category_rec = zhongbamapcategory.objects.filter(sites__id=current_site.id)
    cat_rec = []
    for cat in category_rec:
        data = cat.zhongbadata.filter(sites__id=current_site.id)[:4]

        cat_rec.append({'cat_id':cat.id,'cat_name': cat.name, 'data': data})
    context = {'cat_data': cat_rec,'parent_template': parent_template}

    return render(request, 'zhongba_map_category/index.html', context)