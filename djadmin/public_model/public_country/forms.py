from django import forms
from .models import PublicCountry


class CategoryForm(forms.ModelForm):
    class Meta:
        model = PublicCountry
        fields = "__all__"
