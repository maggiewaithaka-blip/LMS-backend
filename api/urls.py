from users.views import RegistrationAPIView, LoginAPIView
from rest_framework import routers
from django.urls import path, include
from users.views import UserViewSet, ProfileFileUploadView
from courses.views import (
    CourseViewSet,
    CourseCategoryViewSet,
    CourseSectionViewSet,
    CourseModuleViewSet,
    LessonViewSet,
)
from enrollment.views import EnrollmentViewSet, EnrollmentMethodViewSet
from assignments.views import AssignmentViewSet, SubmissionViewSet, AssignmentGradeViewSet, AssignmentListView
from quizzes.views import QuizViewSet, QuestionViewSet, QuizAttemptViewSet, QuestionResponseViewSet, QuizListView
from grades.views import GradeItemViewSet, GradeViewSet
from messaging.views import MessageViewSet, NotificationViewSet
from storage.views import FileViewSet
from courses.views_resource import CourseResourceViewSet
from users.views_application import StudentApplicationView

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'categories', CourseCategoryViewSet)
router.register(r'sections', CourseSectionViewSet)
router.register(r'modules', CourseModuleViewSet)
router.register(r'enrollments', EnrollmentViewSet)
router.register(r'enrollment-methods', EnrollmentMethodViewSet)
router.register(r'assignments', AssignmentViewSet)
router.register(r'submissions', SubmissionViewSet)
router.register(r'assignment-grades', AssignmentGradeViewSet)
router.register(r'quizzes', QuizViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'quiz-attempts', QuizAttemptViewSet)
router.register(r'question-responses', QuestionResponseViewSet)
router.register(r'grade-items', GradeItemViewSet)
router.register(r'grades', GradeViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'files', FileViewSet)

# Register lessons as a nested route under courses
from rest_framework_nested import routers as nested_routers
course_router = nested_routers.NestedDefaultRouter(router, r'courses', lookup='course')
course_router.register(r'lessons', LessonViewSet, basename='course-lessons')
from users.views import ProfileViewSet, RoleViewSet
from rest_framework import permissions

router.register(r'profiles', ProfileViewSet)
router.register(r'roles', RoleViewSet)


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('auth/register/', RegistrationAPIView.as_view(), name='auth_register'),
    path('auth/login/', LoginAPIView.as_view(), name='auth_login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
    path('student-applications/', StudentApplicationView.as_view(), name='student-application'),
    path('courses/<int:course_id>/quizzes/', QuizListView.as_view(), name='course-quizzes'),
    path('courses/<int:course_id>/assignments/', AssignmentListView.as_view(), name='course-assignments'),
    path('users/me/upload/<str:field_name>/', ProfileFileUploadView.as_view(), name='profile-file-upload'),
    path('', include(course_router.urls)),
]
