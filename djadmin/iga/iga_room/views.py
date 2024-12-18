import json
import os
import openpyxl
from .models import iga_room
from rest_framework import generics
from rest_framework import permissions
from .serializers import IgaroomSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
from django_filters import rest_framework
from django.views.generic import DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sites.models import Site
from django.http import HttpResponse
from base.models import get_template
from django.conf import settings

parent_template = get_template()
current_site = Site.objects.get_current()
User = get_user_model()


class DataList(generics.ListCreateAPIView):
    queryset = iga_room.objects.filter(sites__id=current_site.id)
    serializer_class = IgaroomSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = ['title','']

    # 将request.user与author绑定
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DataDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = iga_room.objects.filter(sites__id=current_site.id)
    serializer_class = IgaroomSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

