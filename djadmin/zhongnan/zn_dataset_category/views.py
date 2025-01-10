import markdown
from .models import ZNDatasetCategory
from rest_framework import generics
from rest_framework import permissions
from .serializers import CategorySerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
from django_filters import rest_framework
from django.views.generic import ListView
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..zn_event_category.models import ZNEventCategory

User = get_user_model()


class CategoryList(generics.ListCreateAPIView):
    queryset = ZNDatasetCategory.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = ['name', ]

    # 将request.user与author绑定
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ZNDatasetCategory.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class CategoryListView(ListView):
    model = ZNDatasetCategory
    context_object_name = 'zn_category'
    Category = ZNDatasetCategory.objects.all()


def Categorylist(request):
    all_cat = ZNDatasetCategory.objects.all()
    context = {'Category': all_cat}
    return render(request, 'zn_category/category_list.html', context)


def CategoryIndex(request, pk):
    all_cat = ZNDatasetCategory.objects.all()
    context = {'Category': all_cat}
    return render(request, 'zn_category/category_index.html', context)


def CategoryDataList(request, pk):
    category_rec = get_object_or_404(ZNDatasetCategory, pk=pk)
    all_cat = ZNDatasetCategory.objects.all()
    data_recs = category_rec.zn_dataset.all()
    # 转换列表中的Markdown内容
    # data_recs = [markdown.markdown(data.cnt_md) for data in data_recs_all]

    paginator = Paginator(data_recs, 20)  # 实例化一个分页对象, 每页显示10个
    page = request.GET.get('page')  # 从URL通过get页码，如?page=3
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)  # 如果传入page参数不是整数，默认第一页
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    is_paginated = True if paginator.num_pages > 1 else False  # 如果页数小于1不使用分页

    context = {'data': page_obj, 'cat_name': category_rec.name, 'is_paginated': is_paginated, 'Category': all_cat}
    return render(request, 'zn_category/data_list.html', context)


# 查询指定数量的从第一个到倒数第二个的记录


def index(request):
    category_rec = ZNDatasetCategory.objects.all().order_by('-create_time')

    cat_rec = []
    for cat in category_rec:
        data = cat.zn_dataset.all()[:4]

        cat_rec.append({'cat_id': cat.id, 'cat_name': cat.name, 'data': data})

    event_category_count = ZNEventCategory.objects.all().count() 
    # event_category_rec = ZNEventCategory.objects.all().order_by('order')[:event_category_count - 1]
    event_category_rec = ZNEventCategory.objects.all().order_by('order')

    event_rec = []
    for cat in event_category_rec:
        data = cat.zn_event.all()[:4]
        event_rec.append({'cat_id': cat.id, 'cat_name': cat.name, 'data': data})

    new_event_category = ZNEventCategory.objects.all().order_by('order').last()
    new_event_rec = []
    new_event_data = new_event_category.zn_event.all()[:10]
    new_event_rec.append({'cat_id': new_event_category.id, 'cat_name': new_event_category.name, 'data': new_event_data})

    last_info = new_event_rec[-1]

    context = {'cat_data': cat_rec, 'event_data': event_rec, 'new_event_data': new_event_rec,'new_info':last_info}

    return render(request, 'zn_category/index.html', context)
