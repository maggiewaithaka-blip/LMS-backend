from rest_framework.permissions import BasePermission, SAFE_METHODS


class RolePermission(BasePermission):
    """Permission that allows safe methods to anyone, and restricts unsafe
    methods to users with specific roles defined on the view.

    Expected on the view (optional):
      - `write_roles`: iterable of role names allowed to perform non-safe methods.

    Behavior:
      - If request.method in SAFE_METHODS -> allow
      - If user is superuser -> allow
      - If view has `write_roles`, the user must have at least one of those roles.
      - Otherwise deny.
    """

    def has_permission(self, request, view):
        # Allow read-only methods for everyone
        if request.method in SAFE_METHODS:
            return True

        # Require authentication for unsafe methods
        user = request.user
        if not user or not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        write_roles = getattr(view, 'write_roles', None)
        if not write_roles:
            # If no roles specified, require authenticated users
            return True

        # Use user's helper methods if available
        has_any = False
        try:
            has_any = user.has_any_role(write_roles)
        except Exception:
            # If helper not available fallback to checking related userrole set
            from users.models import UserRole

            has_any = UserRole.objects.filter(user=user, role__name__in=write_roles).exists()

        return has_any
