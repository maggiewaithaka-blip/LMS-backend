from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Assignment, Submission, AssignmentGrade
from .serializers import AssignmentSerializer, SubmissionSerializer, AssignmentGradeSerializer
from users.permissions import RolePermission
from users.permissions_obj import IsCourseTeacherOrOwner

class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all().order_by('id')
    serializer_class = AssignmentSerializer
    permission_classes = [IsCourseTeacherOrOwner]



class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all().order_by('id')
    serializer_class = SubmissionSerializer
    # Object-level permission: owner/teacher can manage submissions; students can create their own
    permission_classes = [IsCourseTeacherOrOwner]



class AssignmentGradeViewSet(viewsets.ModelViewSet):
    queryset = AssignmentGrade.objects.all().order_by('id')
    serializer_class = AssignmentGradeSerializer
    # Only teachers/admins should assign grades
    permission_classes = [RolePermission]
    write_roles = ['teacher', 'admin']




# List assignments for a specific course
from rest_framework.permissions import IsAuthenticatedOrReadOnly
class AssignmentListView(generics.ListAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        course_id = self.kwargs.get('course_id')
        return Assignment.objects.filter(course_id=course_id).order_by('id')
