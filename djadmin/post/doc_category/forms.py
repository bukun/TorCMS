from django import forms
from .models import DocumentCatagory


class CategoryForm(forms.ModelForm):
    class Meta:
        model = DocumentCatagory
        fields = "__all__"
