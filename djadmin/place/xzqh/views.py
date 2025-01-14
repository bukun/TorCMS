import requests
import json
from place.geofea.models  import XZQH
from rest_framework import generics
from rest_framework import permissions
from .serializers import ApiAppSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
from django_filters import rest_framework
from django.shortcuts import render
User = get_user_model()


class DataList(generics.ListCreateAPIView):
    queryset = XZQH.objects.all()
    serializer_class = ApiAppSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = ['name', ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DataDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = XZQH.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

def map_view(request):
    recs = XZQH.objects.values_list('zoning','name','content','parent').distinct()

    recs_list = list(set(recs))

    data_recs = []
    par_rec=''
    sun_rec=''
    for rec in recs_list:

        if rec[3]==None: #(parent)
            par_rec=rec
        else:
            sun_rec=XZQH.objects.filter(parent=rec[3])

        all_rec={par_rec:par_rec,sun_rec:sun_rec}
        if all_rec in data_recs:
            pass
        else:
            data_recs.append(all_rec)


    context = {'all_recs': data_recs}

    return render(request, 'xzqh/map_view.html', context)

def map_simple(request):
    return render(request, 'xzqh/simple.html')
def test(request):
    return render(request, 'xzqh/test.html')