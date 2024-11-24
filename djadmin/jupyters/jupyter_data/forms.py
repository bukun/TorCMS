from django import forms
from .models import Jupyter


class SharedFileForm(forms.ModelForm):
    class Meta:
        model = Jupyter
        fields = ['file', 'title']