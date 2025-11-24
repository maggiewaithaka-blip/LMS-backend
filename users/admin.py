from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Role, UserRole, Profile
# StudentApplication admin removed (student applications handled outside public API)
# from .models_application import StudentApplication
#@admin.register(StudentApplication)
#class StudentApplicationAdmin(admin.ModelAdmin):
#    list_display = ('full_name', 'email', 'nationality', 'highest_academic_qualification', 'submitted_at', 'status')
#    readonly_fields = ('submitted_at',)
#    search_fields = ('full_name', 'email', 'nationality')


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    pass


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'shortname')


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'assigned_at')


## Profile admin disabled — profile management will be handled from backend only
#@admin.register(Profile)
#class ProfileAdmin(admin.ModelAdmin):
#    list_display = (
#        'user', 'profile_picture', 'passport_photo', 'national_id', 'passport',
#        'academic_certificate', 'date_of_birth', 'gender', 'address',
#        'qualification_level', 'field_of_study', 'nationality',
#    )
#    fields = (
#        'user', 'profile_picture', 'passport_photo', 'national_id', 'passport',
#        'academic_certificate', 'date_of_birth', 'gender', 'address',
#        'qualification_level', 'field_of_study', 'nationality',
#    )
#    readonly_fields = ('user',)
