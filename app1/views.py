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


class OrganizationViewSet(viewsets.ModelViewSet):
  queryset = Organization.objects.all()
  serializer_class = OrganizationSerializer

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
  queryset = CustomUser.objects.filter(type="NU")
  serializer_class = CustomUserSerializer

  def create(self, request):
    serializer = CustomUserSerializer(data=request.data)
    print(serializer.is_valid())
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
  print(1)
  if request.method == "POST":
    print(2)
    try:
      user = CustomUser.objects.get(phone=request.data['phone'])
      print(3)
      if user.is_active:
        login(request, user)
        data = {
          "status": 1,
          "data": {
            "id": user.id,
            "firstname": user.first_name,
            "lastname": user.last_name,
            "email": user.email,
            "phone": user.phone,
            "type": user.type,
            "is_active": user.is_active,
            "org": user.org.id
          },
          "message": [],
        }
      else:
        data = {
          "status": 0,
          "data": None,
          "message": ["You are not a active user"],
        }
      return Response(data)
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


class SuperUserModelViewSet(viewsets.ModelViewSet):
  queryset = CustomUser.objects.filter(type="SA")
  serializer_class = CustomUserSerializer

  def list(self, request):
    queryset = CustomUser.objects.filter(type="SA")
    serializer = CustomUserSerializer(queryset, many=True)
    data = {
      "status": 1,
      "data": serializer.data,
      "message": [],
    }
    return Response(data)


class OrgUserModelViewSet(viewsets.ModelViewSet):
  queryset = CustomUser.objects.filter(type="OA")
  serializer_class = CustomUserSerializer

  def list(self, request):
    queryset = CustomUser.objects.filter(type="OA")
    serializer = CustomUserSerializer(queryset, many=True)
    data = {
      "status": 1,
      "data": serializer.data,
      "message": [],
    }
    return Response(data)


def product_upload(request):
  print("In the Product Upload")
  return HttpResponse("In the product uplaod function")
 