from django.db import models

# Create your models here.
class StudentRecord(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    major = models.CharField(max_length=100)
    gpa = models.FloatField()
    enrollment_date = models.DateField()
    
    class Meta:
        db_table = 'student_records'  # Custom table name to avoid conflicts
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
