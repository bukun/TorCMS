from django import forms
from .models import ResourceCatagory


class CategoryForm(forms.ModelForm):
    class Meta:
        model = ResourceCatagory
        fields = "__all__"
