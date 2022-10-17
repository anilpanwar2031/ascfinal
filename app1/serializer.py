from rest_framework import serializers
from .models import Organization, CustomUser
from rest_framework import generics


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
  id = serializers.ReadOnlyField()

  class Meta:
    model = Organization
    fields = "__all__"


class CustomUserSerializer(serializers.ModelSerializer):

  class Meta:
    model = CustomUser
    fields = [
      "id", "first_name", "last_name", "email", "phone", "org"
    ]
    # fields = "__all__"
