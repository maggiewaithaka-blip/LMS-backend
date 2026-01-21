from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from users.permissions import RolePermission
from users.permissions_obj import IsCourseTeacherOrOwner
from .models import Course, CourseCategory, CourseSection, Assignment, Quiz, Resource, Attachment
from .serializers import (
    CourseSerializer,
    CourseCategorySerializer,
    CourseSectionSerializer,
    AssignmentSerializer,
    QuizSerializer,
    ResourceSerializer,
    AttachmentSerializer,
)
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models_scorm import ScormPackage
from .serializers_scorm import ScormPackageSerializer
import zipfile
import os
from django.conf import settings
from rest_framework.decorators import action
from rest_framework.response import Response


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all().order_by('id')
    serializer_class = AssignmentSerializer
    permission_classes = [IsCourseTeacherOrOwner]

class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all().order_by('id')
    serializer_class = QuizSerializer
    permission_classes = [IsCourseTeacherOrOwner]

class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all().order_by('id')
    serializer_class = ResourceSerializer
    permission_classes = [IsCourseTeacherOrOwner]

class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all().order_by('id')
    serializer_class = AttachmentSerializer
    permission_classes = [IsCourseTeacherOrOwner]


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.filter(visible=True).order_by('id')
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
    serializer_class = CourseSectionSerializer
    permission_classes = [IsCourseTeacherOrOwner]

    def get_queryset(self):
        course_id = self.kwargs.get('course_pk') or self.request.query_params.get('course')
        qs = CourseSection.objects.filter(visible=True).order_by('position')
        if course_id:
            qs = qs.filter(course__pk=course_id)
        return qs


            
        return qs


class EnrolledCoursesViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Course.objects.filter(enrollment__user=user).distinct()
        return Course.objects.none()


class ScormPackageListView(generics.ListAPIView):
    queryset = ScormPackage.objects.all().order_by('-uploaded_at')
    serializer_class = ScormPackageSerializer

class ScormPackageUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
        serializer = ScormPackageSerializer(data=request.data)
        if serializer.is_valid():
            scorm = serializer.save()
            # Extract the zip file
            extract_dir = os.path.join(settings.MEDIA_ROOT, 'scorm', f'scorm_{scorm.pk}')
            os.makedirs(extract_dir, exist_ok=True)
            with zipfile.ZipFile(scorm.zip_file.path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)

            # Find index.html in any subdirectory
            index_path = None
            for root, dirs, files in os.walk(extract_dir):
                if 'index.html' in files:
                    index_path = os.path.join(root, 'index.html')
                    break
            if index_path:
                index_dir = os.path.dirname(index_path)
                    # ...removed debug print...
                scorm.extracted_path = index_dir
            else:
                    # ...removed debug print...
                scorm.extracted_path = extract_dir
            scorm.save()
            return Response(ScormPackageSerializer(scorm).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)