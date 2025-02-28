from django.contrib import admin

# Register your models here.

import datetime

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from .models import *


# 先注册


admin.site.register(TabMember)
admin.site.register(TabPost)

admin.site.register(TabPost2Tag)
admin.site.register(TabPostHist)

admin.site.register(TabReply)

admin.site.register(TabTag)
admin.site.register(TabCollect)
admin.site.register(TabRel)

admin.site.register(TabLink)

admin.site.site_header = 'TorCMS后台管理'
admin.site.site_title = 'TorCMS后台管理'
# admin.site.unregister(Group)

