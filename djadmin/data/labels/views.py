from .models import labels
from rest_framework import generics
from rest_framework import permissions
from .serializers import LabelsSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
from django_filters import rest_framework
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from data.categorys.models import categorys
from django.contrib.sites.models import Site
from base.models import get_template

parent_template = get_template()
current_site = Site.objects.get_current()
User = get_user_model()


class LabelsList(generics.ListCreateAPIView):
    queryset = labels.objects.filter(sites__id=current_site.id)
    serializer_class = LabelsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = ['name']

    # 将request.user与author绑定
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LabelsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = labels.objects.filter(sites__id=current_site.id)
    serializer_class = LabelsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


def LabelDataList(request, pk):
    label_rec = get_object_or_404(labels, pk=pk)
    data_recs = label_rec.dataset.filter(sites__id=current_site.id)
    all_cat = categorys.objects.filter(sites__id=current_site.id)
    context = {'data': data_recs, 'label_name': label_rec.name,'Category':all_cat,'parent_template': parent_template}
    return render(request, 'labels/data_list.html', context)