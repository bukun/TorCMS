from django import forms
from .models import heitumapcategory


class HeituCategoryForm(forms.ModelForm):
    class Meta:
        model = heitumapcategory
        fields = "__all__"
