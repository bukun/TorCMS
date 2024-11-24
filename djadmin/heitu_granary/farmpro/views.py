from .models import farmpro
from rest_framework import generics
from rest_framework import permissions
from .serializers import FarmproSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
from django_filters import rest_framework
from django.views.generic import DetailView
from django.shortcuts import render, redirect, get_object_or_404

User = get_user_model()


class FarmproDataList(generics.ListCreateAPIView):
    queryset = farmpro.objects.all()
    serializer_class = FarmproSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = []

    # 将request.user与author绑定
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FarmproDataDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = farmpro.objects.all()
    serializer_class = FarmproSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

