from .models import dataset
from rest_framework import generics
from rest_framework import permissions
from .serializers import DataSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
from django_filters import rest_framework
from django.views.generic import DetailView
from data.categorys.models import categorys
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sites.models import Site
from base.models import get_template

parent_template = get_template()
current_site = Site.objects.get_current()
User = get_user_model()


class DataList(generics.ListCreateAPIView):
    queryset = dataset.objects.filter(sites__id=current_site.id)
    serializer_class = DataSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = ['title', 'category']

    # 将request.user与author绑定
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DataDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = dataset.objects.filter(sites__id=current_site.id)
    serializer_class = DataSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


def DataDetailView(request, dataid):
    # 从url里获取单个任务的pk值，然后查询数据库获得单个对象
    current_site = Site.objects.get_current()
    data = get_object_or_404(dataset, pk=dataid)
    data_cat = categorys.objects.filter(sites__id=current_site.id)

    return render(request, "dataset/data_detail.html", {"data": data, "Category": data_cat,'site': current_site, 'parent_template': parent_template})