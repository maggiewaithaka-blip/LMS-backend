from users.views import LoginAPIView
from rest_framework import routers
from django.urls import path, include
from users.views import UserViewSet
from courses.views import (
    CourseViewSet,
    CourseCategoryViewSet,
    CourseSectionViewSet,
    EnrolledCoursesViewSet,
)
from enrollment.views import EnrollmentViewSet, EnrollmentMethodViewSet
## Removed assignments view imports
## Removed quizzes view imports
from grades.views import GradeItemViewSet, GradeViewSet
from messaging.views import MessageViewSet, NotificationViewSet
from storage.views import FileViewSet
## Removed CourseResourceViewSet import
from users.views import UserViewSet

# StudentApplicationView removed from public API (student applications handled offline/back-end)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'categories', CourseCategoryViewSet)
router.register(r'sections', CourseSectionViewSet, basename='course-section')
# REMOVED: router.register(r'modules', CourseModuleViewSet) - Modules are now nested
router.register(r'enrollments', EnrollmentViewSet)
router.register(r'enrollment-methods', EnrollmentMethodViewSet)
## Removed assignments router registrations
## Removed quizzes router registrations
router.register(r'grade-items', GradeItemViewSet)
router.register(r'grades', GradeViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'files', FileViewSet)

from rest_framework_nested import routers as nested_routers
course_router = nested_routers.NestedDefaultRouter(router, r'courses', lookup='course')

# ADDED: Register CourseModuleViewSet as a nested route under courses
course_router.register(r'sections', CourseSectionViewSet, basename='course-sections')
## Removed CourseModuleViewSet and LessonViewSet nested routes

from users.views import RoleViewSet
from rest_framework import permissions

# Profile endpoints removed from public API
router.register(r'roles', RoleViewSet)


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('auth/login/', LoginAPIView.as_view(), name='auth_login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/me/', UserViewSet.as_view({'get': 'me'}), name='user-me'),
    path('courses/enrolled/', EnrolledCoursesViewSet.as_view({'get': 'list'}), name='enrolled-courses'),
    path('', include(router.urls)),
    # path('courses/<int:course_id>/quizzes/', QuizListView.as_view()),
    # path('courses/<int:course_id>/assignments/', AssignmentListView.as_view()),
    # Profile upload endpoint disabled (profile management handled by backend)
    path('', include(course_router.urls)),
]