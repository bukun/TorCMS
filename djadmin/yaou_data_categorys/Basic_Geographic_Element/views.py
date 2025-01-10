from .models import Basic_Geographic_Element_Category
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
    queryset = Basic_Geographic_Element_Category.objects.filter(sites__id=current_site.id)
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = ['name', ]

    # 将request.user与author绑定
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Basic_Geographic_Element_Category.objects.filter(sites__id=current_site.id)
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class CategoryListView(ListView):
    model = Basic_Geographic_Element_Category
    context_object_name = 'Basic_Geographic_Element_Category'
    Category = Basic_Geographic_Element_Category.objects.filter(sites__id=current_site.id)


def CategoryIndex(request, pk):
    all_cat = Basic_Geographic_Element_Category.objects.filter(sites__id=current_site.id)



    context = {'Category': all_cat, "parent_template": parent_template}

    return render(request, 'Basic_Geographic_Element_Category/category_index.html', context)





def CategoryDataList(request, pk):
    category_rec = get_object_or_404(Basic_Geographic_Element_Category, pk=pk)
    all_cat = Basic_Geographic_Element_Category.objects.filter(sites__id=current_site.id)
    data_recs = category_rec.dataset.filter(sites__id=current_site.id)
    is_paginated, page_obj = get_paginator(data_recs, request)

    context = {'data': page_obj, 'cat_name': category_rec.name, 'is_paginated': is_paginated, 'Category': all_cat, 'parent_template': parent_template}
    return render(request, 'Basic_Geographic_Element_Category/data_list.html', context)


def index(request):
    category_rec = Basic_Geographic_Element_Category.objects.filter(sites__id=current_site.id).order_by('order')

    cat_rec = []
    for cat in category_rec:
        data = cat.dataset.filter(sites__id=current_site.id)
        if data:
            cat_rec.append({'cat_id': cat.id, 'cat_name': cat.name, 'data': data, 'parent': cat.parent})
    context = {'cat_data': cat_rec, 'parent_template': parent_template}

    return render(request, 'Basic_Geographic_Element_Category/index.html', context)
