import markdown
from ..zn_dataset_category.models import ZNDataset
from rest_framework import generics
from rest_framework import permissions
from .serializers import DataSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
from django_filters import rest_framework
from django.views.generic import DetailView
from zhongnan.zn_dataset_category.models import ZNDatasetCategory
from django.shortcuts import render, redirect, get_object_or_404

User = get_user_model()


class DataList(generics.ListCreateAPIView):
    queryset = ZNDataset.objects.all()
    serializer_class = DataSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = ['title', 'category']

    # 将request.user与author绑定
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DataDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ZNDataset.objects.all()
    serializer_class = DataSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


def DataDetailView(request, dataid):
    # 从url里获取单个任务的pk值，然后查询数据库获得单个对象
    data = get_object_or_404(ZNDataset, pk=dataid)
    data_cat = ZNDatasetCategory.objects.all()
    # data.cnt_md = markdown.markdown(data.cnt_md,
    #                                  extensions=[
    #                                   'markdown.extensions.extra',
    #                                   'markdown.extensions.codehilite',
    #                                   'markdown.extensions.toc',
    #                               ],
    #                               safe_mode=True,
    #                               enable_attributes=False)
    return render(request, "zn_dataset/data_detail.html", {"data": data, "Category": data_cat})
