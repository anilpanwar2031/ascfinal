from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from .models import Organization, CustomUser, Product, TestSubmission
from .serializer import OrganizationSerializer, CustomUserSerializer, ProductSerializer, TestSubmissionSerializer
import io
from django.contrib.auth import login
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django_filters import rest_framework


# Create your views here.
def index(request):
  return HttpResponse("Hey")


class TestSubmissionViewSet(viewsets.ModelViewSet):
  queryset = TestSubmission.objects.all().order_by('id')
  serializer_class = TestSubmissionSerializer

  # filter_backends = (rest_framework.DjangoFilterBackend, )
  # filterset_fields = '__all__'

  class Meta:
    ordering = ['-id']


class RequestUserViewSet(viewsets.ModelViewSet):
  queryset = CustomUser.objects.all().order_by('id')
  serializer_class = CustomUserSerializer
  filter_backends = (rest_framework.DjangoFilterBackend, )
  filterset_fields = '__all__'

  class Meta:
    ordering = ['-id']


class OrganizationViewSet(viewsets.ModelViewSet):
  queryset = Organization.objects.all().order_by('id')
  serializer_class = OrganizationSerializer
  filter_backends = (rest_framework.DjangoFilterBackend, )
  filterset_fields = '__all__'

  def list(self, request):
    queryset = Organization.objects.all().order_by('id')
    serializer = OrganizationSerializer(queryset, many=True)
    data = {
      "status": 1,
      "data": serializer.data,
      "message": [],
    }
    return Response(data)


class CustomUserModelViewSet(viewsets.ModelViewSet):
  queryset = CustomUser.objects.filter(type="NU").order_by('id')
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
  queryset = Product.objects.all().order_by('id')
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
      if user.is_active:
        login(request, user)
        if user.type == "SA":
          data = {
            "status": 1,
            "data": {
              "id": user.id,
              "firstname": user.first_name,
              "lastname": user.last_name,
              "email": user.email,
              "phone": user.phone,
              "type": user.type,
              "org": user.org.id if user.org else None,
              "org_name": user.org.name if user.org else None,
              "is_active": user.is_active,
            },
            "message": [""],
          }
        elif user.type == "OA":
          if not user.org:
            data = {
              "status": 0,
              "data": None,
              "message": ["Organization not assigned"],
            }
            return Response(data)
          data = {
            "status": 1,
            "data": {
              "id": user.id,
              "firstname": user.first_name,
              "lastname": user.last_name,
              "email": user.email,
              "phone": user.phone,
              "type": user.type,
              "org": user.org.id,
              "org_name": user.org.name,
              "is_active": user.is_active,
            },
            "message": [""],
          }

        elif user.type == "NU":
          if not user.org:
            data = {
              "status": 0,
              "data": None,
              "message": ["Organization not assigned"],
            }
            return Response(data)
          data = {
            "status": 1,
            "data": {
              "id": user.id,
              "firstname": user.first_name,
              "lastname": user.last_name,
              "email": user.email,
              "phone": user.phone,
              "type": user.type,
              "org": user.org.id,
              "org_name": user.org.name,
              "is_active": user.is_active,
            },
            "message": [""],
          }
        return Response(data)

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
  queryset = CustomUser.objects.filter(type="SA").order_by('id')
  serializer_class = CustomUserSerializer

  def list(self, request):
    queryset = CustomUser.objects.filter(type="SA").order_by('id')
    serializer = CustomUserSerializer(queryset, many=True)
    data = {
      "status": 1,
      "data": serializer.data,
      "message": [],
    }
    return Response(data)


class OrgUserModelViewSet(viewsets.ModelViewSet):
  queryset = CustomUser.objects.filter(type="OA").order_by('id')
  serializer_class = CustomUserSerializer

  def list(self, request):
    queryset = CustomUser.objects.filter(type="OA").order_by('id')
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
