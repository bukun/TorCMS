from .models import ChangChunProject
from rest_framework import generics
from rest_framework import permissions
from .serializers import GeofeaSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
from django_filters import rest_framework
from django.shortcuts import render, redirect, get_object_or_404

User = get_user_model()


class DataList(generics.ListCreateAPIView):

    queryset = ChangChunProject.objects.all()
    serializer_class = GeofeaSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = ['cadastre_id',]

    # 将request.user与author绑定
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DataDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = ChangChunProject.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)



def apppage(request):
    res = ChangChunProject.objects.all()
    return render(request, 'app_list.html',{'resinfo':res,})

def DataDetailView(request, pk):
    # 从url里获取单个任务的pk值，然后查询数据库获得单个对象
    data = get_object_or_404(ChangChunProject, pk=pk)

    data_cat = ChangChunProject.objects.all()
    return render(request, "{}.html".format(data.id), {"data": data, "Category": data_cat})