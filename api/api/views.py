from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from rest_framework import viewsets


class FileUploadView(APIView):
    parser_classes = (FileUploadParser,)

    def put(self, request, filename, format=None):
        file_obj = request.data['file']
        with open(filename, 'wb+') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)
        return Response(status=status.HTTP_204_NO_CONTENT)
