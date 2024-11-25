import json
import subprocess
from .models import Document
from rest_framework import generics
from rest_framework import permissions
from .serializers import DataSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
from django_filters import rest_framework
from post.doc_category.models import DocumentCatagory
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse

from django.contrib.sites.models import Site
from base.models import get_template

parent_template = get_template()
current_site = Site.objects.get_current()

User = get_user_model()


class DataList(generics.ListCreateAPIView):
    queryset = Document.objects.filter(sites__id=current_site.id)
    serializer_class = DataSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = ['title', 'category']

    # 将request.user与author绑定
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DataDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.filter(sites__id=current_site.id)
    serializer_class = DataSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


def DataDetailView(request, pk):
    # 从url里获取单个任务的pk值，然后查询数据库获得单个对象
    data = get_object_or_404(Document, pk=pk)

    data_cat = DocumentCatagory.objects.filter(sites__id=current_site.id)

    return render(request, "document/data_detail.html",
                  {"data": data, "Category": data_cat, "parent_template": parent_template})


def DataSpiderUpdate(request):
    # Document.objects.filter(sites__id=current_site.id).delete()#删除原数据

    subprocess.Popen('scrapy crawl itcast')
    return HttpResponse('ok')


def save_doc(request):
    with open('xx_teachers.json', 'r') as f:
        recs = json.load(f)
        for rec in recs:
            m = Document(title=rec['title'], cnt_md=rec['cnt_md'])
            m.save()
    return HttpResponse('ok')
