from django import forms
from .models import zhongmengmapcategory


class ZhongmengCategoryForm(forms.ModelForm):
    class Meta:
        model = zhongmengmapcategory
        fields = "__all__"
