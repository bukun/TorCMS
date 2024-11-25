from django.urls import path
from black_html.sphinx_doc.views import document_list

urlpatterns = [
    path('', document_list, name='document_list'),
]
