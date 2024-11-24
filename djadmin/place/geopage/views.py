from .models import GeoPage
from rest_framework import generics
from rest_framework import permissions
from .serializers import GeoPageSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
from django_filters import rest_framework

User = get_user_model()


class DataList(generics.ListCreateAPIView):
    queryset = GeoPage.objects.all()
    serializer_class = GeoPageSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    permission_classes = (permissions.AllowAny,)

    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = ['txt','title']

    # 将request.user与author绑定
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DataDetail(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = GeoPageSerializer
    queryset = GeoPage.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    # permission_classes = (permissions.AllowAny,)


