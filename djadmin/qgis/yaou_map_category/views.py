from .models import yaoumapcategory
from rest_framework import generics
from rest_framework import permissions
from .serializers import YaouMapCategorySerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
from django_filters import rest_framework
from django.views.generic import ListView
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from crawl.crawl_label.models import CrawlLabel
from crawl.crawl_document_en.models import CrawlDocumentEN
from qgis.qgis_map.models import qgismap
from data.categorys.models import categorys
from jupyters.jupyter_data.models import Jupyter
from data.dataset.models import dataset
from django.contrib.sites.models import Site
from base.models import get_template

parent_template = get_template()
current_site = Site.objects.get_current()
User = get_user_model()


class YaouMapCategoryList(generics.ListCreateAPIView):
    queryset = yaoumapcategory.objects.filter(sites__id=current_site.id)
    serializer_class = YaouMapCategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = ['name', ]

    # 将request.user与author绑定
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class YaouMapCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = yaoumapcategory.objects.filter(sites__id=current_site.id)
    serializer_class = YaouMapCategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class YaouMapCategoryListView(ListView):
    model = yaoumapcategory
    context_object_name = 'Category'


def YaouMapCategoryIndex(request):
    all_cat = yaoumapcategory.objects.filter(sites__id=current_site.id)
    context = {'Category': all_cat,'parent_template': parent_template}
    return render(request, 'yaou_map_category/category_index.html', context)


def YaouMapCategoryDataList(request, pk):
    category_rec = get_object_or_404(yaoumapcategory, pk=pk)
    all_cat = yaoumapcategory.objects.filter(sites__id=current_site.id)
    data_recs = category_rec.yaoudata.filter(sites__id=current_site.id)
    paginator = Paginator(data_recs, 20)  # 实例化一个分页对象, 每页显示10个
    page = request.GET.get('page')  # 从URL通过get页码，如?page=3
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)  # 如果传入page参数不是整数，默认第一页
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    is_paginated = True if paginator.num_pages > 1 else False  # 如果页数小于1不使用分页

    context = {'data': page_obj, 'cat_name': category_rec.name, 'is_paginated': is_paginated, 'Category': all_cat,'parent_template': parent_template}
    return render(request, 'yaou_map_category/data_list.html', context)


def index(request):
    category_rec = yaoumapcategory.objects.filter(sites__id=current_site.id)
    cat_rec = []
    for cat in category_rec:
        qgis_list = qgismap.objects.filter(yaoucategory=cat,sites__id=current_site.id).exclude(id__isnull=True)

        if len(qgis_list) > 0:
            qgis_rec = qgis_list[:6]
            cat_rec.append({'cat_id': cat.id, 'cat_name': cat.name, 'data': qgis_rec})

    crawl_rec = CrawlLabel.objects.filter(sites__id=current_site.id)
    crawl_arr = []
    for cat in crawl_rec:
        data_list = CrawlDocumentEN.objects.filter(label=cat, valid=1).exclude(id__isnull=True)

        if len(data_list) > 0:
            data_rec = data_list[:6]
            crawl_arr.append({'cat_id': cat.id, 'cat_name': cat.name, 'data': data_rec})

    dataset_category_rec = categorys.objects.filter(sites__id=current_site.id)

    dataset_cat_rec = []
    for data_cat in dataset_category_rec:
        data = data_cat.dataset.filter(sites__id=current_site.id)[:6]
        if data:
            dataset_cat_rec.append({'cat_id': data_cat.id, 'cat_name': data_cat.name, 'data': data, 'parent': data_cat.parent})



    context = {'cat_data': cat_rec, 'crawl_data': crawl_arr,'dataset_cat_data': dataset_cat_rec,'parent_template': parent_template}

    return render(request, 'yaou_map_category/index.html', context)
def yaou_index(request):
    category_rec = yaoumapcategory.objects.filter(sites__id=current_site.id)
    cat_rec = []
    for cat in category_rec:
        qgis_list = qgismap.objects.filter(yaoucategory=cat,sites__id=current_site.id).exclude(id__isnull=True)

        if len(qgis_list) == 6:
            cat_rec.append(qgis_list)



    datalist = dataset.objects.filter(sites__id=current_site.id,category__isnull=False)[:6]


    jupyter_data = Jupyter.objects.filter(sites__id=current_site.id,category__isnull=False)[:6]

    context = {'qgis_data': cat_rec, 'dataset_data': datalist,  'jupyter_data': jupyter_data,'parent_template': parent_template}


    return render(request, 'yaou_map_category/yaou_index.html', context)
def map_index(request):
    category_rec = yaoumapcategory.objects.filter(sites__id=current_site.id)
    cat_rec = []
    for cat in category_rec:
        data = cat.yaoudata.filter(sites__id=current_site.id)[:6]

        cat_rec.append({'cat_id':cat.id,'cat_name': cat.name, 'data': data})
    context = {'cat_data': cat_rec,'parent_template': parent_template}

    return render(request, 'yaou_map_category/map_index.html', context)
def big_index(request):


    return render(request, 'yaou_map_category/big_index.html',)