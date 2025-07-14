from django.db import models
from django.contrib.auth.models import User

class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    expertise = models.CharField(max_length=100, blank=True)
    office_hours = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='instructor_profiles/', blank=True, null=True)
    date_joined = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Course(models.Model):
    LEVEL_CHOICES = [
        ('BEG', 'Beginner'),
        ('INT', 'Intermediate'),
        ('ADV', 'Advanced'),
    ]
    
    title = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    credits = models.PositiveSmallIntegerField(default=3)
    level = models.CharField(max_length=3, choices=LEVEL_CHOICES, default='BEG')
    instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL, null=True, related_name='courses')
    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True)
    max_students = models.PositiveIntegerField(default=30)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.code}: {self.title}"
    
    class Meta:
        ordering = ['code']

class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('ENR', 'Enrolled'),
        ('DRP', 'Dropped'),
        ('CMP', 'Completed'),
    ]
    
    GRADE_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('F', 'F'),
        ('I', 'Incomplete'),
        ('W', 'Withdrawn'),
        ('IP', 'In Progress'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default='ENR')
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES, blank=True, null=True)
    last_activity = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student.username} - {self.course.code}"
    
    class Meta:
        unique_together = ['student', 'course']
        ordering = ['-enrollment_date']
