from .models import apiapp
from rest_framework import generics
from rest_framework import permissions
from .serializers import ApiAppSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
from django_filters import rest_framework
from django.views.generic import DetailView

from django.shortcuts import render, redirect, get_object_or_404

User = get_user_model()


class DataList(generics.ListCreateAPIView):
    queryset = apiapp.objects.all()
    serializer_class = ApiAppSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = ['title',]

    # 将request.user与author绑定
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DataDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = apiapp.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)



def apppage(request):
    res = apiapp.objects.all()
    return render(request, 'app_list.html',{'resinfo':res,})
def DataDetailView(request, pk):
    # 从url里获取单个任务的pk值，然后查询数据库获得单个对象
    print(pk)
    data = get_object_or_404(apiapp, pk=pk)
    print(data.app_id)
    data_cat = apiapp.objects.all()
    return render(request, "{}.html".format(data.app_id), {"data": data, "Category": data_cat})