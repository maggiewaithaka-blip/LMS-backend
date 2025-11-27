from users.views import LoginAPIView, UserViewSet, RoleViewSet
from courses.views import (
    CourseViewSet,
    CourseCategoryViewSet,
    CourseSectionViewSet,
    EnrolledCoursesViewSet,
)
from enrollment.views import EnrollmentViewSet, EnrollmentMethodViewSet
from grades.views import GradeItemViewSet, GradeViewSet
from messaging.views import MessageViewSet, NotificationViewSet
from storage.views import FileViewSet

from rest_framework import routers
from rest_framework_nested import routers as nested_routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path, include

# 1. Main Router - Using explicit basenames to prevent naming collisions
router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'roles', RoleViewSet, basename='role')
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'categories', CourseCategoryViewSet, basename='category')
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')
router.register(r'enrollment-methods', EnrollmentMethodViewSet, basename='enrollment-method')
router.register(r'grade-items', GradeItemViewSet, basename='grade-item')
router.register(r'grades', GradeViewSet, basename='grade')
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'files', FileViewSet, basename='file')


# 2. Nested Router - Ensuring the nested basename is also unique
# This router is nested under the 'courses' prefix defined in the main router
course_router = nested_routers.NestedDefaultRouter(router, r'courses', lookup='course')
# 'course-section-nested' ensures no clash with any globally defined 'section' viewset
course_router.register(r'sections', CourseSectionViewSet, basename='course-section-nested')


urlpatterns = [
    # Auth and Token paths
    path('auth/login/', LoginAPIView.as_view(), name='auth_login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Custom paths linked to ViewSets
    path('users/me/', UserViewSet.as_view({'get': 'me'}), name='user-me'),
    path('courses/enrolled/', EnrolledCoursesViewSet.as_view({'get': 'list'}), name='enrolled-courses'),
    
    # Include main router URLs
    path('', include(router.urls)),
    
    # Include nested router URLs
    path('', include(course_router.urls)),
]