'''
导入科学数据集的元数据，以及数据实体
'''

import os
import json
import pathlib
from openpyxl import load_workbook
import django
import uuid
from pathlib import Path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
if django.VERSION >= (1, 7):  # 自动判断版本
    django.setup()


def update_data():
    from django.contrib.sites.models import Site

    from bigscreen.bigscreen_data.models import BigScreenMapCategory,BigScreenData
    from data.dataset.models import dataset,categorys,labels
    from data.map.models import map
    from dresource.resource_dataset.models import Resource,ResourceCatagory,ResourceLabel
    from jupyters.jupyter_data.models import Jupyter,JupyterCatagory
    from layerstyle.lgeojson.models import lgeojson
    from layerstyle.lprogram.models import lprogram
    from literature.literature_data.models import Literature,LiteratureLabel,LiteratureCatagory
    from pages.page.models import ThePage
    from post.document.models import Document,DocumentCatagory,DocLabel
    from post.topic.models import Topic
    from qgis.qgis_map.models import QgisLabel, qgismap, zhongmengmapcategory,yaoumapcategory,heitumapcategory,zhongbamapcategory,ANSOMapCategory

    site_rec = Site.objects.filter(id=1).values()

    set_value(site_rec,BigScreenMapCategory)
    set_value(site_rec,BigScreenData)

    set_value(site_rec,dataset)
    set_value(site_rec,categorys)
    set_value(site_rec,labels)
    set_value(site_rec,map)

    set_value(site_rec,Resource)
    set_value(site_rec,ResourceCatagory)
    set_value(site_rec,ResourceLabel)

    set_value(site_rec,Jupyter)
    set_value(site_rec,JupyterCatagory)

    set_value(site_rec,lgeojson)
    set_value(site_rec,lprogram)

    set_value(site_rec,Literature)
    set_value(site_rec,LiteratureLabel)
    set_value(site_rec,LiteratureCatagory)

    set_value(site_rec, ThePage)

    set_value(site_rec,Document)
    set_value(site_rec,DocumentCatagory)
    set_value(site_rec,DocLabel)
    set_value(site_rec,Topic)

    set_value(site_rec,Topic)

    set_value(site_rec,ANSOMapCategory)
    set_value(site_rec,zhongbamapcategory)
    set_value(site_rec,heitumapcategory)
    set_value(site_rec,yaoumapcategory)
    set_value(site_rec,zhongmengmapcategory)
    set_value(site_rec,QgisLabel)
    set_value(site_rec,qgismap)




def set_value(site_rec,zhongmengmapcategory):
    zhongmengcategory = zhongmengmapcategory.objects.all()
    for zm_cat in zhongmengcategory:
        zm_cat.sites.add(site_rec.first()['id'])


if __name__ == '__main__':
    update_data()
