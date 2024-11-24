from .models import lgeojson
from rest_framework import generics
from rest_framework import permissions
from .serializers import lgeojsonSerializer
from django.contrib.auth import get_user_model
from django_filters import rest_framework
from django.contrib.sites.models import Site
from base.models import get_template

parent_template = get_template()
current_site = Site.objects.get_current()
User = get_user_model()


class DataList(generics.ListCreateAPIView):
    queryset = lgeojson.objects.filter(sites__id=current_site.id)
    serializer_class = lgeojsonSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    permission_classes = (permissions.AllowAny,)

    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = ['id','title']

    # 将request.user与author绑定
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DataDetail(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = lgeojsonSerializer
    queryset = lgeojson.objects.filter(sites__id=current_site.id)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    # permission_classes = (permissions.AllowAny,)


