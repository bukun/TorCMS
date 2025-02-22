from django import forms

from qgis.qgis_map.models import zhongbamapcategory


class ZhongbaCategoryForm(forms.ModelForm):
    class Meta:
        model = zhongbamapcategory
        fields = "__all__"
