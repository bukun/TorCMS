from django import forms
from .models import BigScreenMapCategory


class BigScreenCategoryForm(forms.ModelForm):
    class Meta:
        model = BigScreenMapCategory
        fields = "__all__"
