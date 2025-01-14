from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from ..crawl_source.models import CrawlDocument
from .resources import DataResource
from django.db import models
from django.forms import TextInput, Textarea
class Documenttadmin(ImportExportModelAdmin):
    resource_class = DataResource
    list_display = ("id","title", "source",  "update_time", "crawlurl", "update_date", "state", "valid", "edit_count","logo")
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'style': 'width: 80%;'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 6, 'style': 'width: 80%;'})},
    }
    list_filter = ("source", "label","state","valid")
    list_display_links = ("title",)
    ordering = ["-update_time","-create_time", "state"]
    list_per_page = 20
    filter_horizontal = ('label',)
    search_fields = ('id','title', 'cnt_md')



# 注册app的admin
admin.site.register(CrawlDocument, Documenttadmin)
