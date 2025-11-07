from rest_framework import routers
from django.urls import path, include
from users.views import UserViewSet
from courses.views import (
    CourseViewSet,
    CourseCategoryViewSet,
    CourseSectionViewSet,
    CourseModuleViewSet,
)
from enrollment.views import EnrollmentViewSet, EnrollmentMethodViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from assignments.views import AssignmentViewSet, SubmissionViewSet, AssignmentGradeViewSet
from quizzes.views import QuizViewSet, QuestionViewSet, QuizAttemptViewSet, QuestionResponseViewSet
from grades.views import GradeItemViewSet, GradeViewSet
from messaging.views import MessageViewSet, NotificationViewSet
from storage.views import FileViewSet
from courses.views_resource import CourseResourceViewSet
from users.views import RegisterView, ChangePasswordView

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
router.register(r'course-resources', CourseResourceViewSet)
from users.views import ProfileViewSet, RoleViewSet, LogoutView, PasswordResetRequestView, PasswordResetConfirmView
from rest_framework import permissions

router.register(r'profiles', ProfileViewSet)
router.register(r'roles', RoleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    path('auth/change-password/', ChangePasswordView.as_view(), name='auth_change_password'),
    path('auth/logout/', LogoutView.as_view(), name='auth_logout'),
    path('auth/password-reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('auth/password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
