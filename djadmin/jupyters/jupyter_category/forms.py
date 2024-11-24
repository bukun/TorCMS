from django import forms
from .models import JupyterCatagory


class JupyterCatagoryForm(forms.ModelForm):
    class Meta:
        model = JupyterCatagory
        fields = "__all__"
