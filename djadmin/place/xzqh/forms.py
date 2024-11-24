from django import forms
from .models import XZQH


class MyModelForm(forms.ModelForm):
    class Meta:
        model = XZQH
