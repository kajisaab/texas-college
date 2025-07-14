from django.contrib import admin
from .models import StudentRecord

# Register your models here.
@admin.register(StudentRecord)
class StudentRecordAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'major', 'gpa', 'enrollment_date')
    list_filter = ('major', 'enrollment_date')
    search_fields = ('first_name', 'last_name', 'email', 'major')
    ordering = ('last_name', 'first_name')
