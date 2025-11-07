from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsCourseTeacherOrOwner(BasePermission):
    """Object-level permission to only allow course owners or teachers of the course
    to edit objects. Read-only access is allowed to anyone.
    Works for Course, CourseSection, CourseModule, Submission, AssignmentGrade, etc.
    """

    def has_object_permission(self, request, view, obj):
        # Allow safe methods for any request
        if request.method in SAFE_METHODS:
            return True

        user = request.user
        if not user or not user.is_authenticated:
            return False

        # superusers can do anything
        if user.is_superuser:
            return True

        # Determine course from object
        course = None
        try:
            # Course itself
            from courses.models import Course
            if isinstance(obj, Course):
                course = obj
            else:
                # CourseSection -> section.course
                if hasattr(obj, 'course'):
                    course = obj.course
                elif hasattr(obj, 'section') and hasattr(obj.section, 'course'):
                    course = obj.section.course
                elif hasattr(obj, 'assignment') and hasattr(obj.assignment, 'course'):
                    course = obj.assignment.course
                elif hasattr(obj, 'submission') and hasattr(obj.submission, 'assignment') and hasattr(obj.submission.assignment, 'course'):
                    course = obj.submission.assignment.course
        except Exception:
            course = None

        # If course could not be determined, deny
        if not course:
            return False

        # Owner check
        if getattr(course, 'owner', None) == user:
            return True

        # Check enrollment or role-based teacher assignment
        try:
            from enrollment.models import Enrollment
            # check if user is enrolled as teacher
            if Enrollment.objects.filter(user=user, course=course, role__in=['teacher', 'admin']).exists():
                return True
        except Exception:
            pass

        # fallback to role assignment table
        try:
            from users.models import UserRole
            if UserRole.objects.filter(user=user, role__name__in=['teacher', 'admin']).exists():
                return True
        except Exception:
            pass

        return False
