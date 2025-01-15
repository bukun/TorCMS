from ..igais_category.models import igaislabel
from rest_framework import generics
from rest_framework import permissions
from .serializers import IgaisLabelsSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
from django_filters import rest_framework
from django.shortcuts import render
from django.shortcuts import get_object_or_404

User = get_user_model()


class LabelsList(generics.ListCreateAPIView):
    queryset = igaislabel.objects.all()
    serializer_class = IgaisLabelsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = ['name']

    # 将request.user与author绑定
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LabelsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = igaislabel.objects.all()
    serializer_class = IgaisLabelsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


def LabelDataList(request, pk):
    label_rec = get_object_or_404(igaislabel, pk=pk)
    data_recs = label_rec.igaisdata.all()
    context = {'data': data_recs, 'label_name': label_rec.name}
    return render(request, 'label/data_list.html', context)
