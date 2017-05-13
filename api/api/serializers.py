from rest_framework import serializers
from .models import Chart, ChartVersion


class ChartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chart
        fields = ('id', 'name', 'description')


class ChartVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChartVersion
        fields = ('id', 'chart', 'version', 'tgz')
