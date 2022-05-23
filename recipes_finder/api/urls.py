from django.urls import path, include
from rest_framework import routers
from .views import IntegrentViewSet

router = routers.DefaultRouter()
router.register(r'integrents', IntegrentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
