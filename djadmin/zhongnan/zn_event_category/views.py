from .models import ZNEventCategory
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

User = get_user_model()


class CategoryList(generics.ListCreateAPIView):
    queryset = ZNEventCategory.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = ['name', ]

    # 将request.user与author绑定
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ZNEventCategory.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class CategoryListView(ListView):
    model = ZNEventCategory
    context_object_name = 'zn_event_category'
    Category = ZNEventCategory.objects.all()



def CategoryIndex(request, pk):
    all_cat = ZNEventCategory.objects.all().order_by('order')
    context = {'Category': all_cat}
    return render(request, 'zn_event_category/category_index.html', context)


def CategoryDataList(request, pk):
    category_rec = get_object_or_404(ZNEventCategory, pk=pk)
    all_cat = ZNEventCategory.objects.all().order_by('order')
    data_recs = category_rec.zn_event.all()
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
    return render(request, 'zn_event_category/data_list.html', context)


def index(request):
    category_rec = ZNEventCategory.objects.all().order_by('order')

    cat_rec = []
    for cat in category_rec:
        data = cat.zn_event.all()[:4]

        cat_rec.append({'cat_id': cat.id, 'cat_name': cat.name, 'data': data})
    context = {'cat_data': cat_rec}

    return render(request, 'zn_event_category/index.html', context)
