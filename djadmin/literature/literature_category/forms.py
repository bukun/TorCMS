from django import forms
from .models import LiteratureCatagory


class CategoryForm(forms.ModelForm):
    class Meta:
        model = LiteratureCatagory
        fields = "__all__"
