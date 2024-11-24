from .models import map
from rest_framework import generics
from rest_framework import permissions
from .serializers import MapSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
from django_filters import rest_framework
from django.contrib.sites.models import Site
from base.models import get_template

parent_template = get_template()
current_site = Site.objects.get_current()
User = get_user_model()


class MapList(generics.ListCreateAPIView):
    queryset = map.objects.filter(sites__id=current_site.id)
    serializer_class = MapSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = ['title',]

    # 将request.user与author绑定
    def perform_create(self, serializer):
        serializer.save(user_name=self.request.user)


class MapDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = map.objects.filter(sites__id=current_site.id)
    serializer_class = MapSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
