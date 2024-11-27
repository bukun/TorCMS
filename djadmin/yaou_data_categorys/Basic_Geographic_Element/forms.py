from django import forms
from .models import Basic_Geographic_Element_Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Basic_Geographic_Element_Category
        fields = "__all__"
