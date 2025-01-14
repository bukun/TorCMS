from ..literature_category.models import Literature
from rest_framework import generics
from rest_framework import permissions
from .serializers import literatureSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
from django_filters import rest_framework
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from literature.literature_category.models import LiteratureCatagory
from django.contrib.sites.models import Site
from base.models import get_template,get_paginator

parent_template = get_template()
current_site = Site.objects.get_current()

User = get_user_model()


class DataList(generics.ListCreateAPIView):
    queryset = Literature.objects.filter(sites__id=current_site.id)
    serializer_class = literatureSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = ['title', 'type']

    # 将request.user与author绑定
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DataDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Literature.objects.filter(sites__id=current_site.id)
    serializer_class = literatureSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


def DataDetailView(request, dataid):
    # 从url里获取单个任务的pk值，然后查询数据库获得单个对象
    data = get_object_or_404(Literature, pk=dataid)
    data_cat = LiteratureCatagory.objects.filter(sites__id=current_site.id)
    return render(request, "literature/data_detail.html", {"data": data ,"Category": data_cat,'parent_template': parent_template})

def Index(request):


    data_recs = Literature.objects.filter(sites__id=current_site.id)
    is_paginated, page_obj = get_paginator(data_recs, request)

    context = {'data': page_obj,'is_paginated': is_paginated,'parent_template': parent_template}
    return render(request, 'literature/data_list.html', context)
