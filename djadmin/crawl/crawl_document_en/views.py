import markdown
import difflib
from .models import CrawlDocumentEN, RzLog
from rest_framework import generics
from rest_framework import permissions
from .serializers import DataSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
from django_filters import rest_framework
from crawl.crawl_source.models import CrawlSource
from crawl.crawl_label.models import CrawlLabel
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

from django.db.models import Count
from bs4 import BeautifulSoup

User = get_user_model()


class DataList(generics.ListCreateAPIView):
    queryset = CrawlDocumentEN.objects.all()
    serializer_class = DataSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = ['title', 'category']

    # 将request.user与author绑定
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DataDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CrawlDocumentEN.objects.all()
    serializer_class = DataSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


def DataDetailView(request, dataid):
    # 从url里获取单个任务的pk值，然后查询数据库获得单个对象
    data = get_object_or_404(CrawlDocumentEN, pk=dataid)

    all_category = CrawlLabel.objects.annotate(num_posts=Count('crawl_document_en')).filter(num_posts__gt=0)
    cat_arr=[]
    for cat in all_category:
        data_list=CrawlDocumentEN.objects.filter(label=cat, valid=1).exclude(id__isnull=True)
        if data_list:
            cat_arr.append(cat)
    config = {
        'codehilite': {
            'use_pygments': False,
            'css_class': 'prettyprint linenums', }
    }
    data.cnt_md = markdown.markdown(data.cnt_md, extensions=['codehilite'], extension_configs=config)
    return render(request, "crawl_docen/data_detail.html", {"data": data, "Category": cat_arr})




def compare_content(request, content1, content2):
    content1 = content1.split("\n")
    content2 = content2.split("\n")
    b = difflib.HtmlDiff()
    r = b.make_file(fromlines=content1, tolines=content2)
    sp = BeautifulSoup(r, 'lxml')
    style = sp.find('style')
    style.string += ".nowrap{width:50%;word-break:break-all;}"
    html = sp.prettify()
    html = html.replace('nowrap="nowrap"', 'class="nowrap"')

    return render(request, 'crawl_docen/compare_content.html',
                  {'con_html': html})
