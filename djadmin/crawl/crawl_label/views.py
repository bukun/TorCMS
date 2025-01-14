from ..crawl_source.models import CrawlLabel,CrawlDocumentEN,CrawlDocument
from rest_framework import generics
from rest_framework import permissions
from .serializers import LabelsSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
from django_filters import rest_framework
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from base.models import get_paginator
User = get_user_model()
from django.db.models import Q


class LabelsList(generics.ListCreateAPIView):
    queryset = CrawlLabel.objects.all()
    serializer_class = LabelsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = ['name']

    # 将request.user与author绑定
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LabelsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CrawlLabel.objects.all()
    serializer_class = LabelsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


def LabelsIndex(request, pk):
    all_cat = CrawlLabel.objects.annotate(num_posts=Count('crawl_document_en')).filter(num_posts__gt=0)

    context = {'Category': all_cat}
    return render(request, 'crawl_label/category_index.html', context)


def LabelsDataList(request, pk):
    label_rec = get_object_or_404(CrawlLabel, pk=pk)
    all_cat = CrawlLabel.objects.annotate(num_posts=Count('crawl_document_en')).filter(num_posts__gt=0)
    cat_arr = []
    for cat in all_cat:
        if CrawlDocumentEN.objects.filter(label=cat, valid=1).exclude(id__isnull=True):
            cat_arr.append(cat)
    data_recs = CrawlDocument.objects.filter(label=label_rec, valid=1)
    is_paginated, page_obj = get_paginator(data_recs, request)

    context = {'data': page_obj, 'cat_name': label_rec.name, 'is_paginated': is_paginated, 'Category': cat_arr}
    return render(request, 'crawl_label/data_list.html', context)


def LabelsDataListEN(request, pk):
    label_rec = get_object_or_404(CrawlLabel, pk=pk)
    all_cat = CrawlLabel.objects.annotate(num_posts=Count('crawl_document_en')).filter(num_posts__gt=0)
    cat_arr = []
    for cat in all_cat:
        if CrawlDocumentEN.objects.filter(label=cat, valid=1).exclude(id__isnull=True):
            cat_arr.append(cat)

    data_recs = CrawlDocumentEN.objects.filter(label=label_rec, valid=1)
    is_paginated, page_obj = get_paginator(data_recs, request)

    context = {'data': page_obj, 'cat_name': label_rec.name, 'is_paginated': is_paginated, 'Category': cat_arr}
    return render(request, 'crawl_label/data_list_en.html', context)


def index_en(request):
    label_rec = CrawlLabel.objects.annotate(num_posts=Count('crawl_document_en')).filter(num_posts__gt=0)

    label_rec_list = []
    for cat in label_rec:
        data_list = CrawlDocumentEN.objects.filter(label=cat, valid=1).exclude(id__isnull=True)
        if len(data_list) > 0:
            data_rec = data_list[:4]
            label_rec_list.append({'cat_id': cat.id, 'cat_name': cat.name, 'data': data_rec})
    context = {'cat_data': label_rec_list}

    return render(request, 'crawl_label/index_en.html', context)


def index(request):
    label_rec = CrawlLabel.objects.annotate(num_posts=Count('crawl_document')).filter(num_posts__gt=0)

    label_rec_list = []
    for cat in label_rec:
        data_list = CrawlDocument.objects.filter(label=cat, valid=1).exclude(id__isnull=True)

        if len(data_list) > 0:
            data_rec = data_list[:4]
            label_rec_list.append({'cat_id': cat.id, 'cat_name': cat.name, 'data': data_rec})
    context = {'cat_data': label_rec_list}

    return render(request, 'crawl_label/index.html', context)
