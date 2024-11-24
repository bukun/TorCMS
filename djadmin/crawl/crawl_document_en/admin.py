from django.contrib import admin, messages
from import_export.admin import ImportExportModelAdmin
from .models import CrawlDocumentEN, RzLog
from .resources import DataResource, RZLogResource
from django.db import models
from django.forms import TextInput, Textarea
import datetime
import logging

logger = logging.getLogger(__name__)



class DocumentENtadmin(ImportExportModelAdmin):
    resource_class = DataResource

    # 控制哪些字段会显示在Admin 的修改列表页面中
    list_display = ("id","title", "source",  "update_time", "crawlurl", "update_date", "state", "valid", "edit_count","logo")
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'style': 'width: 80%;'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 6, 'style': 'width: 80%;'})},
    }
    list_filter = ("source", "label","state","valid")
    list_display_links = ("title",)
    # 用来排序
    ordering = ["-update_time", "-create_time", "state"]
    list_per_page = 20
    filter_horizontal = ('label',)
    search_fields = ('id','title', 'cnt_md')

    # actions = ['run_scrapy']  # 将自定义动作名称添加到列表中

    def run_scrapy(self, request, queryset):

        import subprocess

        # Scrapy命令及参数
        command = ['scrapy', 'crawl', 'mappitall']

        try:
            # 运行Scrapy命令并获取输出结果
            result = subprocess.run(command, capture_output=True, text=True)

            if result.returncode == 0:
                print("Scrapy命令成功执行！")

                # 打印输出内容（如果有）
                output = result.stdout.strip()
                if len(output):
                    print("输出内容:\n", output)

            else:
                print("Scrapy命令执行失败！错误信息：\n", result.stderr.strip())
        except FileNotFoundError as e:
            print("未找到Scrapy命令或相关依赖文件！")

    def save_model(self, request, obj, form, change):
        obj.update_user = request.user
        obj.receiver = request.user.username

        # 用于记录数据变化信息
        if form.has_changed():
            change_list = form.changed_data
            logger.info(f'表格数据变化点：{change_list}')

            try:
                changed_dict = form.cleaned_data

                for i in change_list:
                    x = CrawlDocumentEN.objects.values_list(i, flat=True).filter(id=obj.id)  # 原数据库保存的数据
                    y = changed_dict[i]  # 当前新写入的数据
                    # ----------------------------------
                    # 如果有特殊字段需要另外的动作进行处理的，使用下面的部分代码

                    # 当变更审批状态的时候
                    # if i == 'is_jieshou':  # 此处为特别关注的字段，针对此字段的变动如果需要有其他的操作，可以在此处进行设置相关动作
                    #     obj.jieshou_date = datetime.datetime.now()
                    #     if not y:
                    #         pass  # 设定特殊动作
                    #     else:
                    #         pass
                    # elif i == 'is_doubt':
                    #     if y == 1:
                    #         pass  # 设定特殊动作
                    #     else:
                    #         pass  # 设定特殊动作
                    # else:
                    #     pass  # 设定特殊动作
                    # ---------------------------------------------------------
                    # 如果不需要特殊字段的处理，跳过 -- 之间的不分代码即可

                    # 将相关数据的变化，写入数据库进行存储
                    doc_id = CrawlDocumentEN.objects.filter(id=obj.id).first() if obj.id else None
                    RzLog.objects.create(sheet='crawldocumenten', user=request.user.username, the_id=doc_id,
                                         the_key=i, old_values=str(x[0]), new_values=str(y), create_user=request.user,
                                         update_user=request.user)

            except  BaseException as e:
                logger.error(f'错误类型是:{e.__class__.__name__}\n错误原因: {e}')
                # logger.error(f'详细错误信息a:{traceback.format_exc()}')

        super().save_model(request, obj, form, change)


class RZLogAdmin(ImportExportModelAdmin):
    resource_class = RZLogResource
    # 控制哪些字段会显示在Admin 的修改列表页面中
    list_display = ("sheet", "the_id", "the_key", "update_user",)
    ordering = ["create_time", "sheet"]
    list_per_page = 20


# 注册app的admin
admin.site.register(CrawlDocumentEN, DocumentENtadmin)
admin.site.register(RzLog, RZLogAdmin)
