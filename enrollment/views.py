from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Enrollment, EnrollmentMethod
from .serializers import EnrollmentSerializer, EnrollmentMethodSerializer
from users.permissions import RolePermission


class EnrollmentViewSet(viewsets.ModelViewSet):

    queryset = Enrollment.objects.all().order_by('id')
    serializer_class = EnrollmentSerializer
    permission_classes = [RolePermission]
    write_roles = ['admin', 'teacher', 'student']

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class EnrollmentMethodViewSet(viewsets.ModelViewSet):
    queryset = EnrollmentMethod.objects.all().order_by('id')
    serializer_class = EnrollmentMethodSerializer
    permission_classes = [RolePermission]
    write_roles = ['admin']
