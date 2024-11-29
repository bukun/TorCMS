from django import forms
from .models import LiteratureAuthor


class CategoryForm(forms.ModelForm):
    class Meta:
        model = LiteratureAuthor
        fields = "__all__"
