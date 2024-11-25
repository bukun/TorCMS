from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.conf import settings
import os
# Create your views here.
from django.shortcuts import render
from black_html.sphinx_doc.models import Document_sphinx

def sphinx_document_list(request):
    documents = Document_sphinx.objects.all()
    return render(request, 'document_list.html', {'documents': documents})
def sphinx_docs(request):
    docs_root = getattr(settings, 'SPHINX_DOCS_ROOT', None)
    doc_path = os.path.join(docs_root, 'index.html')
    print(doc_path)
    if docs_root and os.path.exists(doc_path):
        with open(doc_path, 'rb') as f:
            content = f.read()
        return HttpResponse(content, content_type='text/html')
    else:
        return HttpResponse("Sphinx documentation not found.")