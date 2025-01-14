from django import forms
from qgis.qgis_map.models import zhongmengmapcategory


class ZhongmengCategoryForm(forms.ModelForm):
    class Meta:
        model = zhongmengmapcategory
        fields = "__all__"
