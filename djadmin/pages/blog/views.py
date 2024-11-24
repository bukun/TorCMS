from .models import Page
from rest_framework import generics
from rest_framework import permissions
from .serializers import PageSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
from django_filters import rest_framework
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.sites.models import Site

current_site = Site.objects.get_current()

User = get_user_model()


class PageList(generics.ListCreateAPIView):
    queryset = Page.objects.filter(sites__id=current_site.id)
    serializer_class = PageSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = ['title']

    # 将request.user与author绑定
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Page.objects.filter(sites__id=current_site.id)
    serializer_class = PageSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


def PageDetailView(request, cur_slug):
    data = Page.objects.filter(slug=cur_slug).first()
    return render(request, "page/page_detail.html", {"data": data, })
