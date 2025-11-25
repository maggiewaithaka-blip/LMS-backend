from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Course, CourseCategory, CourseSection, CourseModule, Lesson
from .serializers import (
    CourseSerializer,
    CourseCategorySerializer,
    CourseSectionSerializer,
    CourseModuleSerializer,
    LessonSerializer,
)
from users.permissions import RolePermission
from users.permissions_obj import IsCourseTeacherOrOwner
from rest_framework.decorators import action
from rest_framework.response import Response


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by('id')
    serializer_class = CourseSerializer
    # Use object-level permission for course edits
    permission_classes = [IsCourseTeacherOrOwner]

    def perform_create(self, serializer):
        course = serializer.save()
        # Auto-enroll the creator as a teacher for the course
        user = getattr(self.request, 'user', None)
        if user and user.is_authenticated:
            try:
                # Avoid circular imports at module load time
                from users.models import Role, UserRole
                from enrollment.models import Enrollment

                role_obj, _ = Role.objects.get_or_create(name='teacher')
                UserRole.objects.get_or_create(user=user, role=role_obj)
                Enrollment.objects.get_or_create(user=user, course=course, role='teacher')
            except Exception:
                # Don't let auto-enroll failure break course creation; log in real app
                pass


class CourseCategoryViewSet(viewsets.ModelViewSet):
    queryset = CourseCategory.objects.all().order_by('id')
    serializer_class = CourseCategorySerializer
    permission_classes = [RolePermission]
    write_roles = ['admin']


class CourseSectionViewSet(viewsets.ModelViewSet):
    queryset = CourseSection.objects.all().order_by('id')
    serializer_class = CourseSectionSerializer
    permission_classes = [IsCourseTeacherOrOwner]



class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer
    permission_classes = [IsCourseTeacherOrOwner]

    def get_queryset(self):
        course_id = self.kwargs.get('course_pk') or self.request.query_params.get('course')
        qs = Lesson.objects.all().order_by('position')
        if course_id:
            qs = qs.filter(course_id=course_id)
        return qs


class CourseModuleViewSet(viewsets.ModelViewSet):
    queryset = CourseModule.objects.all().order_by('id')
    serializer_class = CourseModuleSerializer
    permission_classes = [IsCourseTeacherOrOwner]


class EnrolledCoursesViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Course.objects.filter(enrollment__user=user).distinct()
        return Course.objects.none()
