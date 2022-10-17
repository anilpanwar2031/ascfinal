from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from .models import Organization, CustomUser
from .serializer import OrganizationSerializer, CustomUserSerializer
import io
from django.contrib.auth import login
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


# Create your views here.
def index(request):
  return HttpResponse("Hey")


class OrganizationViewSet(viewsets.ModelViewSet):
  queryset = Organization.objects.all()
  serializer_class = OrganizationSerializer


class CustomUserModelViewSet(viewsets.ModelViewSet):
  queryset = CustomUser.objects.all()
  serializer_class = CustomUserSerializer


@api_view(['GET', 'POST'])
def loging(request):
  if request.method == "POST":
    try:
      user = CustomUser.objects.get(phone=request.data['phone'])
      login(request, user)
      data = {
            "phone": user.phone,
             }
    except Exception:
      data={"phone": ['Not Found']}
    return Response(data)
  return Response({"phone": ""})
