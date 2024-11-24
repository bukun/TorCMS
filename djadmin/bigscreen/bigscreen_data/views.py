from .models import BigScreenData
from rest_framework import generics
from rest_framework import permissions
from .serializers import BigScreenSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
from django_filters import rest_framework
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.sites.models import Site

current_site = Site.objects.get_current()
User = get_user_model()


class PageList(generics.ListCreateAPIView):
    # queryset = BigScreenData.objects.all()
    queryset = BigScreenData.objects.filter(sites__id=current_site.id)
    serializer_class = BigScreenSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = ['title']

    # 将request.user与author绑定
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PageDetail(generics.RetrieveUpdateDestroyAPIView):
    # queryset = BigScreenData.objects.all()
    # 只筛选域名为筛选域名的网站用
    queryset = BigScreenData.objects.filter(sites__id=current_site.id)
    serializer_class = BigScreenSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
