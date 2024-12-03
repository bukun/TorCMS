import json
from django.shortcuts import render
from .models import Photoinfo
from rest_framework import generics
from rest_framework import permissions
from .serializers import PhotoinfoSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
from django_filters import rest_framework


User = get_user_model()
# Create your views here.


class DataList(generics.ListCreateAPIView):
    queryset = Photoinfo.objects.all()
    serializer_class = PhotoinfoSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = ['location_name', ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DataDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Photoinfo.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
