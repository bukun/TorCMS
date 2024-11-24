from django import forms
from django.contrib.gis.db.models import PointField
from django.contrib.gis.forms import PointField as GisPointField
from .models import PlanarFeatures

class CustomPointField(GisPointField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget.attrs['style'] = 'width: 1000px;'  # 设置宽度为400px


class MyModelForm(forms.ModelForm):
    location = CustomPointField(widget=forms.TextInput)

    class Meta:
        model = PlanarFeatures
        fields = ['location']