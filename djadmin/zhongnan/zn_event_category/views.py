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
from base.models import get_paginator
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
    is_paginated, page_obj = get_paginator(data_recs, request)

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
