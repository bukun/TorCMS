from django.shortcuts import render

from django.http import HttpResponse


def my_custom_view(request):

    return HttpResponse("Hello from Wagtail custom view!")