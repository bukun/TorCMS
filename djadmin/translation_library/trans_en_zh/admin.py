import json
import requests
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import TranslationENZH
from .resources import ApiAppResource
from django.db import models
from django.forms import TextInput, Textarea
from django.shortcuts import render, redirect, get_object_or_404


class TranslationENZHAdmin(ImportExportModelAdmin):
    resource_class = ApiAppResource
    # 控制哪些字段会显示在Admin 的修改列表页面中
    list_display = ("id", "text_en", "trans_zh","edit_count")
    # 用来排序

    list_per_page = 20

    search_fields = ('text_en', 'trans_zh')

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'style': 'width: 80%;'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 6, 'style': 'width: 80%;'})},
    }

    # actions = ['run_translation']  # 将自定义动作名称添加到列表中

    def run_translation(self, request, queryset):

        for rec in request.POST.get('_selected_action'):

            data = TranslationENZH.objects.filter(id=rec).first()

            trans_text = data.text_en

            try:
                if not trans_text:
                    res = {'status': 1, 'info': '未输入查询内容'}
                    print("1" * 50)
                    print(res)
                else:
                    headers = {
                        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
                    }
                    parmas = {'kw': trans_text}
                    response = requests.post(url='https://fanyi.baidu.com/sug', params=parmas, headers=headers)
                    print("ok " * 20)

                    if (json.loads(response.text)['data']):
                        res = {'status': 0, 'info': json.loads(response.text)['data'][0]['v']}

                        TranslationENZH.objects.filter(id=rec).update(trans_zh=res['info'])
                        # return res
                        # return HttpResponse(json.dumps(res))
            except:
                res = {'status': 2, 'info': '未查询到结果，请输入正确的内容'}
                print("2" * 50)
                print(res)
    run_translation.short_description = ' 翻译'
    run_translation.icon = 'fas fa-language'

# 注册app的admin
admin.site.register(TranslationENZH, TranslationENZHAdmin)
