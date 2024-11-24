from django import forms
from .models import zhongbamapcategory


class ZhongbaCategoryForm(forms.ModelForm):
    class Meta:
        model = zhongbamapcategory
        fields = "__all__"
