from .models import farmproavg
from rest_framework import generics
from rest_framework import permissions
from .serializers import FarmproAvgSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
from django_filters import rest_framework
from django.views.generic import DetailView
from django.shortcuts import render, redirect, get_object_or_404

User = get_user_model()


class FarmproAvgDataList(generics.ListCreateAPIView):
    queryset = farmproavg.objects.all()
    serializer_class = FarmproAvgSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = []

    # 将request.user与author绑定
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FarmproAvgDataDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = farmproavg.objects.all()
    serializer_class = FarmproAvgSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

