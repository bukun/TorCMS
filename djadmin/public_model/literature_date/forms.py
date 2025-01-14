from django import forms
from public_model.literature_author.models import LiteratureDate


class CategoryForm(forms.ModelForm):
    class Meta:
        model = LiteratureDate
        fields = "__all__"
