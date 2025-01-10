from .models import ANSOMapCategory
from rest_framework import generics
from rest_framework import permissions
from .serializers import ANSOMapCategorySerializer
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


class ANSOMapCategoryList(generics.ListCreateAPIView):
    queryset = ANSOMapCategory.objects.filter(sites__id=current_site.id)
    serializer_class = ANSOMapCategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = ['name', ]

    # 将request.user与author绑定
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ANSOMapCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ANSOMapCategory.objects.filter(sites__id=current_site.id)
    serializer_class = ANSOMapCategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class ANSOMapCategoryListView(ListView):
    model = ANSOMapCategory
    context_object_name = 'Category'


def ANSOMapCategoryIndex(request):
    all_cat = ANSOMapCategory.objects.filter(sites__id=current_site.id)
    context = {'Category': all_cat,'parent_template': parent_template}
    return render(request, 'anso_map_category/category_index.html', context)


def ANSOMapCategoryDataList(request, pk):
    category_rec = get_object_or_404(ANSOMapCategory, pk=pk)
    all_cat = ANSOMapCategory.objects.filter(sites__id=current_site.id)
    data_recs = category_rec.ansodata.filter(sites__id=current_site.id)
    is_paginated, page_obj = get_paginator(data_recs, request)

    context = {'data': page_obj, 'cat_name': category_rec.name, 'is_paginated': is_paginated, 'Category': all_cat,'parent_template': parent_template}
    return render(request, 'anso_map_category/data_list.html', context)


def index(request):
    category_rec = ANSOMapCategory.objects.filter(sites__id=current_site.id)

    cat_rec = []
    for cat in category_rec:
        data = cat.ansodata.filter(sites__id=current_site.id)[:4]

        cat_rec.append({'cat_id':cat.id,'cat_name': cat.name, 'data': data})
    context = {'cat_data': cat_rec,'parent_template': parent_template}

    return render(request, 'anso_map_category/index.html', context)
