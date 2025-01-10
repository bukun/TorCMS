from .models import ZNDatasetLabel
from rest_framework import generics
from rest_framework import permissions
from .serializers import LabelsSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
from django_filters import rest_framework
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from zhongnan.zn_dataset_category.models import ZNDatasetCategory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
User = get_user_model()


class LabelsList(generics.ListCreateAPIView):
    queryset = ZNDatasetLabel.objects.all()
    serializer_class = LabelsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = ['name']

    # 将request.user与author绑定
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LabelsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ZNDatasetLabel.objects.all()
    serializer_class = LabelsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


def LabelDataList(request, pk):

    label_rec = get_object_or_404(ZNDatasetLabel, pk=pk)
    all_cat = ZNDatasetCategory.objects.all()
    data_recs = label_rec.zn_dataset.all()
    # 转换列表中的Markdown内容
    # data_recs = [markdown.markdown(data.cnt_md) for data in data_recs_all]

    paginator = Paginator(data_recs, 20)  # 实例化一个分页对象, 每页显示10个
    page = request.GET.get('page')  # 从URL通过get页码，如?page=3
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)  # 如果传入page参数不是整数，默认第一页
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    is_paginated = True if paginator.num_pages > 1 else False  # 如果页数小于1不使用分页

    context = {'data': data_recs, 'label_name': label_rec.name, 'is_paginated': is_paginated, 'Category': all_cat}

    return render(request, 'zn_label/data_list.html', context)
