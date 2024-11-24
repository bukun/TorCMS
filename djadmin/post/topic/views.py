from .models import Topic,Comment
from rest_framework import generics
from rest_framework import permissions
from .serializers import DataSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
from django_filters import rest_framework
from django.views.generic import DetailView
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .forms import CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sites.models import Site

current_site = Site.objects.get_current()
User = get_user_model()


class DataList(generics.ListCreateAPIView):
    queryset = Topic.objects.filter(sites__id=current_site.id)
    serializer_class = DataSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = ['title', 'category']

    # 将request.user与author绑定
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DataDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Topic.objects.filter(sites__id=current_site.id)
    serializer_class = DataSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


def DataDetailView(request, pk):
    # 从url里获取单个任务的pk值，然后查询数据库获得单个对象
    data = get_object_or_404(Topic, pk=pk)
    comment_list = Comment.objects.filter(topic_id=pk)  # 从数据库找出该文章的评论数据对象

    comment_form = CommentForm()

    # return render(request, "data_detail.html", {"data": data})
    return render(request, "topic/topic_detail.html",{
        'data': data,
        'comment_list': comment_list,
        'comment_form': comment_form,
    })


def index(request):  # 首页函数
    # if request.user.username:  # 判断用户是否已登录（用户名是否存在）
    topic_list = Topic.objects.filter(sites__id=current_site.id)  # 取出所有的文章对象，结果返回一个QuerySet[]对象

    paginator = Paginator(topic_list, 20)  # 实例化一个分页对象, 每页显示10个
    page = request.GET.get('page')  # 从URL通过get页码，如?page=3
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)  # 如果传入page参数不是整数，默认第一页
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    is_paginated = True if paginator.num_pages > 1 else False  # 如果页数小于1不使用分页

    context = {'topic_list': page_obj,  'is_paginated': is_paginated}

    return render(request, 'topic/index.html', context=context)
    # else:
    #     return redirect('/user_login/')


def article_detail(request, article_id):

    # if request.user.username:
    article = get_object_or_404(Topic, pk=article_id)

    comment_list = Comment.objects.filter(topic_id=article_id)  # 从数据库找出该文章的评论数据对象
    comment_form = CommentForm()


    return render(request, 'topic/topic_detail.html', {"article": article, "comment_list": comment_list,"comment_form":comment_form})  # 返回对应文章的详情页面
    # else:
    #     return redirect('/user_login/')

@csrf_exempt
def comment_control(request):  # 提交评论的处理函数

    # if request.user.username:
    content = request.POST.get('content')
    topic = request.POST.get('topic')
    pid = request.POST.get('parent')
    author_id = request.user.id  # 获取当前用户的ID

    parent=Comment.objects.filter(id=pid).first() if pid else None
    Comment.objects.create(content=content,parent=parent,  topic_id=topic,
                           user_id=author_id)  # 将提交的数据保存到数据库中

    article = list(
        Comment.objects.values('id', 'content', 'parent_id', 'topic_id', 'user_id',
                               'create_time'))  # 以键值对的形式取出评论对象，并且转化为列表list类型

    return JsonResponse(article, safe=False)  # JsonResponse返回JSON字符串，自动序列化，如果不是字典类型，则需要添加safe参数为False
    # else:
    #     return redirect('/user_login/')

# @login_required(login_url='/userprofile/login/')
def post_comment(request, article_id, parent_comment_id=None):
    article = get_object_or_404(Topic, id=article_id)

    # 处理 POST 请求
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user

            # 二级回复
            if parent_comment_id:
                parent_comment = Comment.objects.get(id=parent_comment_id)
                # 若回复层级超过二级，则转换为二级
                new_comment.parent_id = parent_comment.get_root().id
                # 被回复人
                new_comment.reply_to = parent_comment.user
                new_comment.save()
                return HttpResponse('200 OK')

            new_comment.save()
            return redirect(article)
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 处理 GET 请求
    elif request.method == 'GET':
        comment_form = CommentForm()
        context = {
            'comment_form': comment_form,
            'article_id': article_id,
            'parent_comment_id': parent_comment_id
        }
        return render(request, 'comment/reply.html', context)
    # 处理其他请求
    else:
        return HttpResponse("仅接受GET/POST请求。")