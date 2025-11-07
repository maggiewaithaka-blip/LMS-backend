from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import GradeItem, Grade
from .serializers import GradeItemSerializer, GradeSerializer
from users.permissions import RolePermission
from users.permissions_obj import IsCourseTeacherOrOwner


class GradeItemViewSet(viewsets.ModelViewSet):
    queryset = GradeItem.objects.all().order_by('id')
    serializer_class = GradeItemSerializer
    permission_classes = [IsCourseTeacherOrOwner]


class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all().order_by('id')
    serializer_class = GradeSerializer
    permission_classes = [IsCourseTeacherOrOwner]
