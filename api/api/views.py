from rest_framework import viewsets, status
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FileUploadParser
from .models import Chart, ChartVersion
from .serializers import ChartSerializer, ChartVersionSerializer


class ChartViewSet(viewsets.ModelViewSet):

    queryset = Chart.objects.all()
    serializer_class = ChartSerializer
    parser_classes = (MultiPartParser, FileUploadParser,)

    @detail_route(methods=['post'])
    def upload(self, request, pk=None):
        try:
            chart = Chart.objects.get(id=pk)
        except Chart.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        if request.data:
            filename = request.data['file'].name
            # Assuming the filename is like 'name-major.minor.patch.tgz'
            semver2 = '.'.join(filename.rsplit('-')[-1].rsplit('.')[:-1])
            version = ChartVersion(version=semver2, tgz=request.data['file'], chart=chart)
            version.save()
            return Response({}, status=status.HTTP_201_CREATED)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)



class ChartVersionViewSet(viewsets.ModelViewSet):

    queryset = ChartVersion.objects.all()
    serializer_class = ChartVersionSerializer
