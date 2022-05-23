from rest_framework import serializers
from recipe.models import Integrent


class IntegrentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Integrent
        fields = ['name', 'prefered_unit', 'type']
