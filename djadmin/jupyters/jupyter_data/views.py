import nbformat
import requests
from .models import Jupyter
from rest_framework import generics
from rest_framework import permissions
from .serializers import JupyterSerializer
from .permissions import IsOwnerOrReadOnly
from .forms import SharedFileForm
from django.contrib.auth import get_user_model
from django_filters import rest_framework
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from jupyters.jupyter_category.models import JupyterCatagory
from django.contrib.sites.models import Site
from django.http import HttpResponse
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponseRedirect
current_site = Site.objects.get_current()
User = get_user_model()
from base.models import get_template

parent_template = get_template()


class DataList(generics.ListCreateAPIView):
    queryset = Jupyter.objects.filter(sites__id=current_site.id)
    serializer_class = JupyterSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = ['title', ]

    # 将request.user与author绑定
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DataDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Jupyter.objects.filter(sites__id=current_site.id)
    serializer_class = JupyterSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


def DataDetailView(request, dataid):
    # 从url里获取单个任务的pk值，然后查询数据库获得单个对象
    data = get_object_or_404(Jupyter, pk=dataid)
    data_cat = JupyterCatagory.objects.filter(sites__id=current_site.id)
    return render(request, "jupyter_data/data_detail.html",
                  {"data": data, "Category": data_cat, 'parent_template': parent_template})


def ShowShare(request):
    # 获取当前登录用户的UserProfile对象
    profile = User.objects.get(username=request.user.username)

    # 通过UserProfile对象获取所有与当前用户关联的文章
    data_recs = profile.shared_with.filter(sites__id=current_site.id)

    paginator = Paginator(data_recs, 20)  # 实例化一个分页对象, 每页显示10个
    page = request.GET.get('page')  # 从URL通过get页码，如?page=3
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)  # 如果传入page参数不是整数，默认第一页
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    is_paginated = True if paginator.num_pages > 1 else False  # 如果页数小于1不使用分页

    context = {'data': page_obj, 'is_paginated': is_paginated}
    return render(request, "jupyter_data/show_share_list.html", context)


def Index(request):
    data_recs = Jupyter.objects.filter(sites__id=current_site.id)
    paginator = Paginator(data_recs, 20)  # 实例化一个分页对象, 每页显示10个
    page = request.GET.get('page')  # 从URL通过get页码，如?page=3
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)  # 如果传入page参数不是整数，默认第一页
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    is_paginated = True if paginator.num_pages > 1 else False  # 如果页数小于1不使用分页

    context = {'data': page_obj, 'is_paginated': is_paginated, 'parent_template': parent_template}
    return render(request, 'jupyter_data/data_list.html', context)


def SystemIndex(request):
    if str(request.user) == 'AnonymousUser':
        context = {'parent_template': parent_template}
    else:
        data_recs = Jupyter.objects.filter(sites__id=current_site.id, user=request.user)[:8]
        context = {'data': data_recs, 'parent_template': parent_template}

    return render(request, 'jupyter_data/system_index.html', context)


# 打开镜像服务器
def OpenDCSystem(request):
    if request.method == 'POST':
        dc_image = request.POST.get('dc_image')
        user = request.POST.get('user')
        user_info = User.objects.filter(username=user).first()
        data = {
            "image": dc_image,
            "user": user_info.username,
            "mach": user_info.jupyter_url,
            "port": user_info.jupyter_port,
        }
        url3 = "http://pod.igadc.cn/i/"
        response = requests.post(url3, data=data)
        print(response.text)

        return HttpResponseRedirect(f'https://www.baidu.com/')


# 打开特定文件
def OpenSystem(request):
    if request.method == 'POST':
        dc_image = request.POST.get('dc_image')
        user = request.POST.get('user')
        file_id = request.POST.get('file_id')
        user_info = User.objects.filter(username=user).first()

        data = {
            "image": dc_image,
            "jufile": file_id,
            "user": user_info.username,
            "mach": user_info.jupyter_url,
            "port": user_info.jupyter_port,
        }
        url2 = "http://pod.igadc.cn/t/"
        response = requests.post(url2, data=data)
        print(response.text)
        return redirect('https://cms.igadc.cn/')



def upload_file(request):
    if request.method == 'POST':
        form = SharedFileForm(request.POST, request.FILES)
        if form.is_valid():
            shared_file = form.save()
            # 这里可以添加分享逻辑，比如将文件关联到特定用户
            # shared_file.shared_with.add(*some_users*)
            return HttpResponse('File uploaded successfully.')
    else:
        form = SharedFileForm()
    return render(request, 'jupyter_data/upload_file.html', {'form': form, 'parent_template': parent_template})


def download_file(request, file_id):
    shared_file = Jupyter.objects.get(id=file_id)
    # 这里可以添加权限检查逻辑，比如检查是否共享给请求者
    response = HttpResponse(shared_file.file, content_type='application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename="%s"' % shared_file.file.name.split('/')[-1]
    return response
