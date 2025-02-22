from django import forms

from qgis.qgis_map.models import ANSOMapCategory


class ANSOCategoryForm(forms.ModelForm):
    class Meta:
        model = ANSOMapCategory
        fields = "__all__"
