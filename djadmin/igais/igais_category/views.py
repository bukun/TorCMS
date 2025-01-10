from .models import igaiscategory
from rest_framework import generics
from rest_framework import permissions
from .serializers import IgaisCategorySerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
from django_filters import rest_framework
from django.views.generic import ListView
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from base.models import get_paginator
User = get_user_model()


class IgaisCategoryList(generics.ListCreateAPIView):
    queryset = igaiscategory.objects.all()
    serializer_class = IgaisCategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = ['name','order']

    # 将request.user与author绑定
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class IgaisCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = igaiscategory.objects.all()
    serializer_class = IgaisCategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class IgaisCategoryListView(ListView):
    model = igaiscategory
    context_object_name = 'IgaisCategory'

def IgaisCategoryIndex(request, pk):
    all_cat = igaiscategory.objects.filter(kind=pk)
    context = {'Category': all_cat}
    return render(request, 'category/category_index.html', context)


def IgaisCategoryDataList(request, pk):
    category_rec = get_object_or_404(igaiscategory, pk=pk)
    all_cat = igaiscategory.objects.all()
    data_recs = category_rec.igaisdata.all()
    is_paginated, page_obj = get_paginator(data_recs, request)


    context = {'data': page_obj, 'cat_name': category_rec.name, 'is_paginated': is_paginated,'Category':all_cat}
    return render(request, 'category/data_list.html', context)

