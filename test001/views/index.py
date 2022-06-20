from django.shortcuts import render, redirect, HttpResponse


# Create your views here.

def index(request):
    return render(request, "../templates/test/index.html")
