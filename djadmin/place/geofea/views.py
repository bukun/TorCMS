from .models import Geofea
from rest_framework import generics
from rest_framework import permissions
from .serializers import GeofeaSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
from django_filters import rest_framework
from django.views.generic import DetailView

from django.shortcuts import render, redirect, get_object_or_404

User = get_user_model()


class DataList(generics.ListCreateAPIView):
    queryset = Geofea.objects.all()
    serializer_class = GeofeaSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = ['title',]

    # 将request.user与author绑定
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DataDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = Geofea.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

