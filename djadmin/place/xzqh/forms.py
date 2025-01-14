from django import forms
from place.geofea.models  import XZQH


class MyModelForm(forms.ModelForm):
    class Meta:
        model = XZQH
