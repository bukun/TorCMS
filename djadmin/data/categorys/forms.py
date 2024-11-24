from django import forms
from .models import categorys


class CategoryForm(forms.ModelForm):
    class Meta:
        model = categorys
        fields = "__all__"
