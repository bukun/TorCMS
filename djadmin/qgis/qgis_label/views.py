from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.shortcuts import get_object_or_404, render
from django_filters import rest_framework
from rest_framework import generics, permissions

from base.models import get_paginator, get_template
from qgis.qgis_map.models import QgisLabel

from .permissions import IsOwnerOrReadOnly
from .serializers import LabelsSerializer

parent_template = get_template()
current_site = Site.objects.get_current()
User = get_user_model()


class LabelsList(generics.ListCreateAPIView):
    queryset = QgisLabel.objects.filter(sites__id=current_site.id)
    serializer_class = LabelsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = ['name']

    # 将request.user与author绑定
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LabelsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = QgisLabel.objects.filter(sites__id=current_site.id)
    serializer_class = LabelsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


def LabelDataList(request, pk):
    label_rec = get_object_or_404(QgisLabel, pk=pk)
    data_recs = label_rec.qgismap.filter(sites__id=current_site.id)
    is_paginated, page_obj = get_paginator(data_recs, request)
    context = {
        'data': page_obj,
        'is_paginated': is_paginated,
        'label_name': label_rec.name,
        'parent_template': parent_template,
    }
    return render(request, 'qgis_labels/data_list.html', context)
