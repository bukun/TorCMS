import markdown
from .models import CrawlDocument
from rest_framework import generics
from rest_framework import permissions
from .serializers import DataSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
from django_filters import rest_framework
from django.views.generic import DetailView
from crawl.crawl_label.models import CrawlLabel
from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.db.models import Count

User = get_user_model()


class DataList(generics.ListCreateAPIView):
    queryset = CrawlDocument.objects.all()
    serializer_class = DataSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = ['title', 'category']

    # 将request.user与author绑定
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DataDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CrawlDocument.objects.all()
    serializer_class = DataSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)



def DataDetailView(request, dataid):
    # 从url里获取单个任务的pk值，然后查询数据库获得单个对象
    data = get_object_or_404(CrawlDocument, pk=dataid)
    all_category = CrawlLabel.objects.annotate(num_posts=Count('crawl_document')).filter(num_posts__gt=0)
    config = {
        'codehilite': {
            'use_pygments': False,
            'css_class': 'prettyprint linenums', }
    }
    data.cnt_md = markdown.markdown(data.cnt_md, extensions=['codehilite'], extension_configs=config)
    return render(request, "crawl_doc/data_detail.html", {"data": data, "Category": all_category})
