from .models import JumpBtn
from rest_framework import generics
from rest_framework import permissions
from .serializers import BigScreenSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
from django_filters import rest_framework
from django.shortcuts import render
from django.shortcuts import get_object_or_404

User = get_user_model()


class PageList(generics.ListCreateAPIView):
    queryset = JumpBtn.objects.all()
    serializer_class = BigScreenSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = ['name']

    # 将request.user与author绑定
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = JumpBtn.objects.all()
    serializer_class = BigScreenSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


