from django.contrib import admin
from .models import Course, Instructor, Enrollment

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'expertise', 'date_joined')
    search_fields = ('user__first_name', 'user__last_name', 'user__email', 'expertise')
    list_filter = ('expertise', 'date_joined')
    
    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    
    get_full_name.short_description = 'Name'
    get_full_name.admin_order_field = 'user__last_name'

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'credits', 'level', 'instructor', 'start_date', 'end_date', 'is_active')
    list_filter = ('level', 'credits', 'is_active', 'start_date')
    search_fields = ('code', 'title', 'description', 'instructor__user__last_name')
    filter_horizontal = ('prerequisites',)
    list_editable = ('is_active',)
    date_hierarchy = 'start_date'
    
    fieldsets = (
        ('Course Information', {
            'fields': ('title', 'code', 'description', 'credits', 'level')
        }),
        ('Instructor and Prerequisites', {
            'fields': ('instructor', 'prerequisites')
        }),
        ('Enrollment Details', {
            'fields': ('max_students', 'start_date', 'end_date', 'is_active')
        }),
    )

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrollment_date', 'status', 'grade')
    list_filter = ('status', 'grade', 'enrollment_date')
    search_fields = ('student__username', 'student__first_name', 'student__last_name', 'course__code', 'course__title')
    date_hierarchy = 'enrollment_date'
    
    autocomplete_fields = ['student', 'course']
    
    fieldsets = (
        ('Student and Course', {
            'fields': ('student', 'course')
        }),
        ('Enrollment Details', {
            'fields': ('status', 'grade')
        }),
    )
