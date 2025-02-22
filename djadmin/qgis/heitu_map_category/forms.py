from django import forms

from qgis.qgis_map.models import heitumapcategory


class HeituCategoryForm(forms.ModelForm):
    class Meta:
        model = heitumapcategory
        fields = "__all__"
