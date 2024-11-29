from django import forms
from .models import LiteratureDate


class CategoryForm(forms.ModelForm):
    class Meta:
        model = LiteratureDate
        fields = "__all__"
