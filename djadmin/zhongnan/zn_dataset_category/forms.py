from django import forms
from .models import ZNDatasetCategory


class CategoryForm(forms.ModelForm):
    class Meta:
        model = ZNDatasetCategory
        fields = "__all__"
