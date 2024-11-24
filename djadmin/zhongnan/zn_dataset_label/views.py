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
    data_recs = label_rec.zn_dataset.all()
    all_cat = ZNDatasetCategory.objects.all()
    context = {'data': data_recs, 'label_name': label_rec.name,'Category':all_cat}
    return render(request, 'zn_label/data_list.html', context)
