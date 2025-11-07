from django.contrib import admin

from .models import ActivityLog


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'action', 'object_type', 'object_id', 'timestamp')
    list_filter = ('action', 'object_type')
    search_fields = ('user__username', 'action', 'object_id')
    readonly_fields = ('timestamp',)
    # Keep logs read-only in admin
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
