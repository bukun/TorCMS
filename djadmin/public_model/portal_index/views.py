from rest_framework import generics
from rest_framework import permissions
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.sites.models import Site
from post.document.models import Document
from public_model.literature_author.models import LiteratureAuthor
from base.models import get_template
from django.contrib.auth import get_user_model
from django_filters import rest_framework
from django.views.generic import ListView
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.sites.models import Site
from base.models import get_template


parent_template = get_template()
current_site = Site.objects.get_current()
User = get_user_model()

#中蒙俄协同创新平台 http://ydyl.gislab.cn/
def ydyl_index(request):

    post_data = Document.objects.filter(sites__id=current_site.id,category__isnull=False)[:4]
    expert_data = LiteratureAuthor.objects.filter(sites__id=current_site.id)[:3]

    context = {'post_data': post_data, 'expert_data': expert_data, 'parent_template': parent_template}


    return render(request, 'portal_index/ydyl_index.html', context)
