from django import forms
from .models import ANSOMapCategory


class ANSOCategoryForm(forms.ModelForm):
    class Meta:
        model = ANSOMapCategory
        fields = "__all__"
