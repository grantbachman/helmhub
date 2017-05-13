from rest_framework import viewsets
from .models import Chart, ChartVersion
from .serializers import ChartSerializer, ChartVersionSerializer


class ChartViewSet(viewsets.ModelViewSet):

    queryset = Chart.objects.all()
    serializer_class = ChartSerializer


class ChartVersionViewSet(viewsets.ModelViewSet):

    queryset = ChartVersion.objects.all()
    serializer_class = ChartVersionSerializer
