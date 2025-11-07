from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models_resource import CourseResource
from .serializers_resource import CourseResourceSerializer
from users.permissions_obj import IsCourseTeacherOrOwner


class CourseResourceViewSet(viewsets.ModelViewSet):
    queryset = CourseResource.objects.all().order_by('id')
    serializer_class = CourseResourceSerializer
    permission_classes = [IsCourseTeacherOrOwner]
