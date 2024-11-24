from django import forms
from .models import ZNEventCategory


class CategoryForm(forms.ModelForm):
    class Meta:
        model = ZNEventCategory
        fields = "__all__"
