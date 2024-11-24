from django import forms
from .models import CrawlSource


class CategoryForm(forms.ModelForm):
    class Meta:
        model = CrawlSource
        fields = "__all__"
