from .models import TheWiki
from rest_framework import generics
from rest_framework import permissions
from .serializers import PageSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
from django_filters import rest_framework
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.sites.models import Site
from base.models import get_template

parent_template = get_template()
current_site = Site.objects.get_current()

User = get_user_model()


class PageList(generics.ListCreateAPIView):
    queryset = TheWiki.objects.filter(sites__id=current_site.id)
    serializer_class = PageSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = ['title']

    # 将request.user与author绑定
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TheWiki.objects.filter(sites__id=current_site.id)
    serializer_class = PageSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


def PageDetailView(request, cur_slug):
    data = TheWiki.objects.filter(slug=cur_slug).first()
    return render(request, "wiki/wiki_detail.html", {"data": data,'parent_template': parent_template })
