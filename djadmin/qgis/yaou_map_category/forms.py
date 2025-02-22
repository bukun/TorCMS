from django import forms

from qgis.qgis_map.models import yaoumapcategory


class YaouCategoryForm(forms.ModelForm):
    class Meta:
        model = yaoumapcategory
        fields = "__all__"
