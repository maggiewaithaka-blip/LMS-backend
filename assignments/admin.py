from django.contrib import admin
from .models import Attachment

class AttachmentInline(admin.TabularInline):
	model = Attachment
	extra = 1

class AssignmentGradeAdmin(admin.ModelAdmin):
	inlines = [AttachmentInline]

from django.contrib import admin
from .models import Attachment

## Removed Attachment admin registration
