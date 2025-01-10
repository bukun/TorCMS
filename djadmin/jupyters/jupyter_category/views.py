from .models import JupyterCatagory
from rest_framework import generics
from rest_framework import permissions
from .serializers import CategorySerializer
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


class CategoryList(generics.ListCreateAPIView):
    queryset = JupyterCatagory.objects.filter(sites__id=current_site.id)
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = ['name', ]

    # 将request.user与author绑定
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = JupyterCatagory.objects.filter(sites__id=current_site.id)
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class CategoryListView(ListView):
    model = JupyterCatagory
    context_object_name = 'jupyter_category'
    Category = JupyterCatagory.objects.filter(sites__id=current_site.id)


def Categorylist(request):
    all_cat = JupyterCatagory.objects.filter(sites__id=current_site.id)
    context = {'Category': all_cat, 'parent_template': parent_template}
    return render(request, 'jupyter_category/category_list.html', context)


def CategoryIndex(request, pk):
    all_cat = JupyterCatagory.objects.filter(sites__id=current_site.id)
    context = {'Category': all_cat, 'parent_template': parent_template}
    return render(request, 'jupyter_category/category_index.html', context)


def CategoryDataList(request, pk):
    temp = request.GET.get('temp', '0')
    category_rec = get_object_or_404(JupyterCatagory, pk=pk)
    all_cat = JupyterCatagory.objects.filter(sites__id=current_site.id)
    data_recs = category_rec.jupyter_data.filter(sites__id=current_site.id)
    is_paginated, page_obj = get_paginator(data_recs, request)
    if temp == '1':
        p_template = 'jupyter_base.html'
    else:
        p_template = parent_template
    context = {'data': page_obj, 'cat_name': category_rec.name, 'is_paginated': is_paginated, 'Category': all_cat,
               'parent_template': p_template,'jupyter_temp':temp}

    temp_src = 'jupyter_category/data_list.html'

    return render(request, temp_src, context)


def index(request):
    category_rec = JupyterCatagory.objects.filter(sites__id=current_site.id)

    cat_rec = []
    for cat in category_rec:
        data = cat.jupyter_data.filter(sites__id=current_site.id)[:4]

        cat_rec.append({'cat_id': cat.id, 'cat_name': cat.name, 'data': data, 'parent': cat.parent})
    context = {'cat_data': cat_rec, 'parent_template': parent_template}

    return render(request, 'jupyter_category/index.html', context)
