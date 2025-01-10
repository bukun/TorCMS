from .models import ZNEventLabel
from rest_framework import generics
from rest_framework import permissions
from .serializers import LabelsSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
from django_filters import rest_framework
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from zhongnan.zn_event_category.models import ZNEventCategory
from base.models import get_paginator
User = get_user_model()


class LabelsList(generics.ListCreateAPIView):
    queryset = ZNEventLabel.objects.all()
    serializer_class = LabelsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = ['name']

    # 将request.user与author绑定
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LabelsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ZNEventLabel.objects.all()
    serializer_class = LabelsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


def LabelDataList(request, pk):
    label_rec = get_object_or_404(ZNEventLabel, pk=pk)
    data_recs = label_rec.zn_event.all()
    all_cat = ZNEventCategory.objects.all().order_by('order')
    is_paginated, page_obj = get_paginator(data_recs, request)
    context = {'data': page_obj, 'is_paginated': is_paginated,'label_name': label_rec.name,'Category':all_cat}
    return render(request, 'zn_event_label/data_list.html', context)
