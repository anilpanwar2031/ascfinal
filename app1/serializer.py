from rest_framework import serializers
from .models import Organization, CustomUser, Product
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt


class OrganizationSerializer(serializers.ModelSerializer):
  id = serializers.ReadOnlyField()

  class Meta:
    model = Organization
    fields = "__all__"


class CustomUserSerializer(serializers.ModelSerializer):

  class Meta:
    model = CustomUser
    fields = ["id", "first_name", "last_name", "email", "phone", "org"]
  


class ProductSerializer(serializers.ModelSerializer):

  class Meta:
    model = Product
    fields = "__all__"
