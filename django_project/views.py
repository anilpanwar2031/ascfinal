from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.http import FileResponse

# Create your views here.


def index(request):
  return render(request, "homepage.html")
