from rest_framework import serializers
from recipe.models import Integrent, IntegrentType


class IntegrentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntegrentType
        fields = ['name']


class IntegrentSerializer(serializers.ModelSerializer):
    type = IntegrentTypeSerializer()

    class Meta:
        model = Integrent
        fields = ['name', 'prefered_unit', 'type']
