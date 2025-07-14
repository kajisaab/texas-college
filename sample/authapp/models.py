from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    address = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    major = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='student_profiles/', blank=True, null=True)
    date_joined = models.DateField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.student_id})"
    
    class Meta:
        ordering = ['student_id']
