from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import File
from .serializers import FileSerializer


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all().order_by('id')
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
