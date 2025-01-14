from django import forms
from qgis.qgis_map.models import BigScreenMapCategory


class BigScreenCategoryForm(forms.ModelForm):
    class Meta:
        model = BigScreenMapCategory
        fields = "__all__"
