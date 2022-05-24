from django import views
from django.shortcuts import render
from rest_framework import viewsets

from recipe.serializers import IntegrentSerializer, IntegrentTypeSerializer
from recipe.models import Integrent, IntegrentType

# Create your views here.


class IntegrentTypeViewSet(viewsets.ModelViewSet):
    queryset = IntegrentType.objects.all()
    serializer_class = IntegrentTypeSerializer


class IntegrentViewSet(viewsets.ModelViewSet):
    queryset = Integrent.objects.all()
    serializer_class = IntegrentSerializer
