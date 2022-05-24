from django.urls import path, include
from rest_framework import routers
from .views import IntegrentViewSet, IntegrentTypeViewSet

router = routers.DefaultRouter()
router.register(r'integrents', IntegrentViewSet)
router.register(r'integrent-type', IntegrentTypeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
