from .models import TranslationZHEN
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
    queryset = TranslationZHEN.objects.all()
    serializer_class = ApiAppSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = ['title',]

    # 将request.user与author绑定
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DataDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = TranslationZHEN.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)



#
# def youdaofanyi(request):
#     '''
#     有道翻译功能
#     '''
#     import json
#     from urllib import parse
#     import urllib.request, urllib.parse, urllib.request
#     query = {}  # 定义需要翻译的文本
#     fanyi = request.POST.get('fanyi_content', '')
#     query['q'] = fanyi  # 输入要翻译的文本
#     url = 'http://fanyi.youdao.com/openapi.do?keyfrom=11pegasus11&key=273646050&type=data&doctype=json&version=1.1&' + parse.urlencode(
#         query)  # 有道翻译api
#     response = urllib.request.urlopen(url, timeout=3)
#     # response = urllib.parse.urlopen(url)
#
#     # 编码转换
#     try:
#         html = response.read().decode('utf-8')
#         d = json.loads(html)
#         explains = d.get('basic').get('explains')  # 翻译后输出
#         a1 = d.get('basic').get('uk-phonetic')  # 英式发音
#         a2 = d.get('basic').get('us-phonetic')  # 美式发音
#         explains_list = []
#         for result in explains:
#             explains_list.append(result)
#         # 输出
#         fanyi_dict = {
#             'q': query['q'],
#             'yinshi': a1,
#             'meishi': a2,
#             'explains_list': explains_list,
#         }
#         return fanyi_dict
#     except Exception as e:
#         print(e)
#
#
# def fanyi(request):
#     import requests
#     import json
#     content = request.POST.get('content')
#     try:
#         if not content:
#             res={'status':1,'info':'未输入查询内容'}
#             return HttpResponse(json.dumps(res))
#         else:
#             headers = {
#                 'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
#             }
#             parmas = {'kw': content}
#             response = requests.post(url='https://fanyi.baidu.com/sug', params=parmas, headers=headers)
#             print(json.loads(response.text)['data'][0]['v'])
#             res={'status':0,'info':json.loads(response.text)['data'][0]['v']}
#             return HttpResponse(json.dumps(res))
#     except:
#         res={'status':2,'info':'未查询到结果，请输入正确的内容'}
#         return  HttpResponse(json.dumps(res))
