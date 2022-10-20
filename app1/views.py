from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from .models import Organization, CustomUser, Product
from .serializer import OrganizationSerializer, CustomUserSerializer, ProductSerializer
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


class OrganizationViewSet(viewsets.ViewSet):
  queryset = Organization.objects.all()

  def list(self, request):
    queryset = Organization.objects.all()
    serializer = OrganizationSerializer(queryset, many=True)
    data = {
      "status": 1,
      "data": serializer.data,
      "message": [],
    }
    return Response(data)


class CustomUserModelViewSet(viewsets.ModelViewSet):
  queryset = CustomUser.objects.all()
  serializer_class = CustomUserSerializer

  def create(self, request):
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      data = {
        "status": 1,
        "data": serializer.data,
        "message": [],
      }
      return Response(data)
    else:
      data = {
        "status": 0,
        "data": None,
        "message": ["Mobile number already exists"],
      }
      return Response(data)

  def retrieve(self, request, *args, **kwargs):
    try:
      instance = self.get_object()
      serializer = self.get_serializer(instance)
      data = {
        "status": 1,
        "data": serializer.data,
        "message": [],
      }
      return Response(data)
    except:
      data = {
        "status": 0,
        "data": None,
        "message": ["Mobile number already exists"],
      }
      return Response(data)




class ProductViewSet(viewsets.ModelViewSet):
  queryset = Product.objects.all()
  serializer_class = ProductSerializer
  lookup_field = 'sku'

  def create(self, request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      data = {
        "status": 1,
        "data": serializer.data,
        "message": [],
      }
      return Response(data)
    else:
      data = {
        "status": 0,
        "data": None,
        "message": ["Invalid Sku"],
      }
      return Response(data)

  def retrieve(self, request, *args, **kwargs):
    try:
      instance = self.get_object()
      serializer = self.get_serializer(instance)
      data = {
        "status": 1,
        "data": serializer.data,
        "message": [],
      }
      return Response(data)
    except:
      data = {
        "status": 0,
        "data": None,
        "message": ["Invalid Sku"],
      }
      return Response(data)





@api_view(['GET', 'POST'])
def loging(request):
  if request.method == "POST":
    try:
      user = CustomUser.objects.get(phone=request.data['phone'])
      login(request, user)

      data = {
        "status": 1,
        "data": {
          "id": user.id,
          "firstname": user.first_name,
          "lastname": user.last_name,
          "email": user.email,
          "phone": user.phone,
          "org": user.org.id
        },
        "message": [],
      }
    except Exception:
      data = {
        "status": 0,
        "data": None,
        "message": ["Invalid details entered"],
      }
    return Response(data)
  data = {
    "status": 0,
    "data": None,
    "message": ["Invalid details entered"],
  }
  return Response(data)


# Product
@api_view(['GET', 'POST'])
def product(request):
  if request.method == "POST":

    print("/n")
    print("/n")
    print("/n")

    print("In the POST")
    try:
      prod = Product.objects.get(sku=request.data['sku'])

      print("/n")
      print("/n")
      print("/n")
      print("Prod", prod)
      print("In the Try")

      data = {
        "status": 1,
        "data": {
          "id": prod.id,
          "name": prod.name,
          # "organization": prod.organization,
          "test_for": prod.test_for,
          "sku": prod.sku,
        },
        "message": [],
      }
      return Response(data)
    except Exception:
      print("/n")
      print("/n")
      print("/n")
      print("In the Exception")
      data = {
        "status": 0,
        "data": None,
        "message": ["Invalid details entered"],
      }
      return Response(data)

  data = {
    "status": 0,
    "data": None,
    "message": ["Invalid details entered"],
  }
  return Response(data)
