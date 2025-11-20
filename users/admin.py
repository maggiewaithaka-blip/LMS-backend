from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Role, UserRole, Profile
from .models_application import StudentApplication
@admin.register(StudentApplication)
class StudentApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'nationality', 'qualification', 'knqf_level', 'submitted_at', 'status')
    readonly_fields = ('submitted_at',)
    search_fields = ('full_name', 'email', 'nationality')


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    pass


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'shortname')


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'assigned_at')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
