from ..barn_dataset.models import Barnfield
from rest_framework import generics
from rest_framework import permissions
from .serializers import BarnfieldSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
from django_filters import rest_framework
from django.views.generic import DetailView

from django.shortcuts import render, redirect, get_object_or_404
User = get_user_model()


class DataList(generics.ListCreateAPIView):
    queryset = Barnfield.objects.all()
    serializer_class = BarnfieldSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = ['name','fieldid']

    # 将request.user与author绑定
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DataDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Barnfield.objects.all()
    serializer_class = BarnfieldSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


def DataDetailView(request, dataid):
    # 从url里获取单个任务的pk值，然后查询数据库获得单个对象
    data = get_object_or_404(Barnfield, pk=dataid)
    return render(request, "dataset/data_detail.html", {"data": data})
