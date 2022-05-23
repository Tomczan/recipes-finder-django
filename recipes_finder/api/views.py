from django.shortcuts import render
from rest_framework import viewsets

from .serializers import IntegrentSerializer
from recipe.models import Integrent

# Create your views here.


class IntegrentViewSet(viewsets.ModelViewSet):
    queryset = Integrent.objects.all()
    serializer_class = IntegrentSerializer
