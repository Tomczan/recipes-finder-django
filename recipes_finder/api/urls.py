from django.urls import path, include
from rest_framework import routers
from .views import IntegrentViewSet, IntegrentTypeViewSet, RecipeViewSet

router = routers.DefaultRouter()
router.register(r'integrents', IntegrentViewSet)
router.register(r'integrent-type', IntegrentTypeViewSet)
router.register(r'recipe', RecipeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
