from .models import igaisdata
from rest_framework import generics
from rest_framework import permissions
from .serializers import IgaisDataSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
from django_filters import rest_framework
from django.views.generic import DetailView
from igais.igais_category.models import igaiscategory
from django.shortcuts import render, redirect, get_object_or_404

User = get_user_model()


class DataList(generics.ListCreateAPIView):
    queryset = igaisdata.objects.all()
    serializer_class = IgaisDataSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = ['title', 'kind', 'category']

    # 将request.user与author绑定
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DataDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = igaisdata.objects.all()
    serializer_class = igaiscategory
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


def DataDetailView(request, pk):
    # 从url里获取单个任务的pk值，然后查询数据库获得单个对象
    data = get_object_or_404(igaisdata, pk=pk)
    data_cat = igaiscategory.objects.filter(kind=data.kind)
    return render(request, "data/data_detail.html", {"data": data, "Category": data_cat})
