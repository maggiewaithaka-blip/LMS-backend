from rest_framework import generics, permissions
from .models_application import StudentApplication
from .serializers_application import StudentApplicationSerializer

class StudentApplicationView(generics.CreateAPIView):
    queryset = StudentApplication.objects.all()
    serializer_class = StudentApplicationSerializer
    permission_classes = [permissions.AllowAny]
