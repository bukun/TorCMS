from .models import lprogram
from rest_framework import generics
from rest_framework import permissions
from .serializers import lprogramSerializer
from django.contrib.auth import get_user_model
from django_filters import rest_framework
from django.contrib.sites.models import Site

current_site = Site.objects.get_current()
User = get_user_model()


class DataList(generics.ListCreateAPIView):
    queryset = lprogram.objects.filter(sites__id=current_site.id)
    serializer_class = lprogramSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = ['id','title']

    # 将request.user与author绑定
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DataDetail(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = lprogramSerializer
    queryset = lprogram.objects.filter(sites__id=current_site.id)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    # permission_classes = (permissions.AllowAny,)


