from django import forms
from jupyters.jupyter_category.models import Jupyter


class SharedFileForm(forms.ModelForm):
    class Meta:
        model = Jupyter
        fields = ['file', 'title']