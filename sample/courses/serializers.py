from rest_framework import serializers
from .models import Course, Instructor, Enrollment

class InstructorSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    
    class Meta:
        model = Instructor
        fields = ['id', 'name', 'expertise', 'bio']
    
    def get_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

class CourseSerializer(serializers.ModelSerializer):
    instructor = InstructorSerializer(read_only=True)
    level_display = serializers.CharField(source='get_level_display', read_only=True)
    enrolled_students = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'code', 'description', 'credits', 'level', 
                  'level_display', 'instructor', 'max_students', 'enrolled_students',
                  'start_date', 'end_date', 'is_active']
    
    def get_enrolled_students(self, obj):
        return obj.enrollments.filter(status='ENR').count()

class EnrollmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    student_name = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'student_name', 'course', 'enrollment_date', 
                  'status', 'status_display', 'grade']
        read_only_fields = ['student', 'enrollment_date']
    
    def get_student_name(self, obj):
        return f"{obj.student.first_name} {obj.student.last_name}" if obj.student.first_name else obj.student.username