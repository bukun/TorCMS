from .models import CrawlSource
from rest_framework import generics
from rest_framework import permissions
from .serializers import CrawlSourceSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
from django_filters import rest_framework
from django.views.generic import ListView
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from crawl.crawl_source.models import CrawlLabel
from base.models import get_paginator
User = get_user_model()


class CategoryList(generics.ListCreateAPIView):
    queryset = CrawlSource.objects.all()
    serializer_class = CrawlSourceSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = ['title', ]

    # 将request.user与author绑定
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CrawlSource.objects.all()
    serializer_class = CrawlSourceSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class CategoryListView(ListView):
    model = CrawlSource
    context_object_name = 'crawl_source'
    Category = CrawlSource.objects.all()


def Categorylist(request):
    all_cat = CrawlSource.objects.all()
    context = {'Category': all_cat}
    return render(request, 'crawl_source/category_list.html', context)


def CategoryIndex(request, pk):
    all_cat = CrawlSource.objects.all()
    context = {'Category': all_cat}
    return render(request, 'crawl_source/category_index.html', context)


def CategoryDataList(request, pk):
    category_rec = get_object_or_404(CrawlSource, pk=pk)
    all_cat = CrawlLabel.objects.all()
    data_recs = category_rec.crawl_document.all()
    is_paginated, page_obj = get_paginator(data_recs, request)

    context = {'data': page_obj, 'cat_name': category_rec.title, 'is_paginated': is_paginated, 'Category': all_cat}
    return render(request, 'crawl_source/data_list.html', context)


def CategoryDataListEN(request, pk):
    category_rec = get_object_or_404(CrawlSource, pk=pk)
    all_cat = CrawlLabel.objects.all()
    data_recs = category_rec.crawl_document_en.all()
    is_paginated, page_obj = get_paginator(data_recs, request)

    context = {'data': page_obj, 'cat_name': category_rec.title, 'is_paginated': is_paginated, 'Category': all_cat}
    return render(request, 'crawl_source/data_list_en.html', context)


def index_en(request):
    category_rec = CrawlSource.objects.all()

    cat_rec = []
    for cat in category_rec:
        data = cat.crawl_document_en.all()[:4]

        cat_rec.append({'cat_id': cat.id, 'cat_name': cat.title, 'data': data})
    context = {'cat_data': cat_rec}

    return render(request, 'crawl_source/index_en.html', context)


def index(request):
    category_rec = CrawlSource.objects.all()

    cat_rec = []
    for cat in category_rec:
        data = cat.crawl_document.all()[:4]

        cat_rec.append({'cat_id': cat.id, 'cat_name': cat.title, 'data': data})
    context = {'cat_data': cat_rec}

    return render(request, 'crawl_source/index.html', context)
