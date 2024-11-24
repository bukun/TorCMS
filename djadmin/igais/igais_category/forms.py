from django import forms
from .models import igaiscategory


class IgaisCategoryForm(forms.ModelForm):
    class Meta:
        model = igaiscategory
        fields = "__all__"
