from django import forms
from .models import yaoumapcategory


class YaouCategoryForm(forms.ModelForm):
    class Meta:
        model = yaoumapcategory
        fields = "__all__"
