from django.urls import path, include
from rest_framework import routers
from .views import OrganizationViewSet, CustomUserModelViewSet, loging, ProductViewSet
from django.views.decorators.csrf import csrf_exempt

router = routers.DefaultRouter()
router.register(r'organization', OrganizationViewSet)
router.register(r'user', CustomUserModelViewSet)
router.register(r'product', ProductViewSet, basename='product')

urlpatterns = [
  path('', include(router.urls)),
  path("login/", loging),
]
