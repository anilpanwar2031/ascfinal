from rest_framework import serializers
from .models import Organization, CustomUser, Product
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt


class OrganizationSerializer(serializers.ModelSerializer):
  # id = serializers.ReadOnlyField()
  owner_fname = serializers.ReadOnlyField(source='owner.first_name')
  owner_lname = serializers.ReadOnlyField(source='owner.last_name')
  class Meta:
    model = Organization
    read_only_fields = ('id', 'owner_fname', 'owner_lname')
    fields = ["id", "name", "primary_name", "primary_title", "phone", "email", "address",
            "city",
            "state",
            "zip",
            "note",
            "owner",
            "owner_fname",
            "owner_lname"  
    ]


class CustomUserSerializer(serializers.ModelSerializer):
  
  org_name = serializers.ReadOnlyField(source='org.name')
  class Meta:
    model = CustomUser
    read_only_fields = ('id', 'org_name')
    fields = [
      "id", "first_name", "last_name", "email", "phone", "type", "is_active",
      "org", "org_name"
    ]


class ProductSerializer(serializers.ModelSerializer):

  class Meta:
    model = Product
    fields = "__all__"
