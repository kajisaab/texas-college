# Session 7: Hands-on Exercises

## Exercise 1: Extend the Course Management System

In this exercise, you'll extend the course management system by adding new models and functionality.

### Task 1: Create an Assignment Model

Create a new model called `Assignment` with the following fields:

- `title`: CharField (max_length=100)
- `course`: ForeignKey to Course
- `description`: TextField
- `due_date`: DateField
- `points`: PositiveIntegerField
- `file_attachment`: FileField (optional, upload_to='assignments/')
- `is_active`: BooleanField (default=True)

```python
# Add to courses/models.py
class Assignment(models.Model):
    # Your code here
    pass
    
    def __str__(self):
        # Your code here
        pass
```

### Task 2: Create a Submission Model

Create a model to track student submissions for assignments:

```python
class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    submitted_date = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='submissions/')
    comments = models.TextField(blank=True)
    grade = models.PositiveIntegerField(null=True, blank=True)
    
    class Meta:
        # Ensure a student can only submit once per assignment
        # Your code here
        pass
        
    def __str__(self):
        # Your code here
        pass
        
    def is_late(self):
        # Check if submission was after the due date
        # Your code here
        pass
```

### Task 3: Register Models with Admin

Customize the admin interface for the new models:

```python
# Add to courses/admin.py
@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    # Your code here - add appropriate list_display, list_filter, search_fields
    pass
    
@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    # Your code here - add appropriate list_display, list_filter, search_fields
    # Add a custom method to display if submission is late
    pass
```

### Task 4: Create Views and Templates

Create views and templates to:

1. List all assignments for a course
2. Display assignment details
3. Allow students to submit assignments
4. Show a student's submissions

```python
# Add to courses/views.py
def assignment_list(request, course_id):
    # Your code here
    pass
    
def assignment_detail(request, assignment_id):
    # Your code here
    pass
    
def submit_assignment(request, assignment_id):
    # Your code here - handle form submission
    pass
    
def my_submissions(request):
    # Your code here - show all submissions for the logged-in student
    pass
```

### Task 5: Update URLs

Add URL patterns for the new views:

```python
# Add to courses/urls.py
path('course/<int:course_id>/assignments/', views.assignment_list, name='assignment_list'),
path('assignment/<int:assignment_id>/', views.assignment_detail, name='assignment_detail'),
path('assignment/<int:assignment_id>/submit/', views.submit_assignment, name='submit_assignment'),
path('my-submissions/', views.my_submissions, name='my_submissions'),
```

## Exercise 2: Advanced Querying

Create a new file `courses/queries.py` with functions that demonstrate advanced ORM usage:

```python
from django.db.models import Avg, Count, Sum, Q, F
from .models import Course, Enrollment, Instructor, Assignment, Submission

def get_popular_courses(min_students=5):
    """Return courses with more than min_students enrollments"""
    # Your code here - use annotate and Count
    pass
    
def get_course_stats():
    """Return a dictionary with various course statistics"""
    # Your code here - calculate:
    # - Total number of active courses
    # - Average number of students per course
    # - Course with most prerequisites
    # - Instructor with most courses
    pass
    
def get_student_progress(student_id):
    """Return statistics about a student's progress"""
    # Your code here - calculate:
    # - Number of courses enrolled
    # - Number of completed courses
    # - Average grade across all courses
    # - Number of assignments submitted on time vs. late
    pass
    
def complex_filter_example():
    """Demonstrate complex filtering with Q objects"""
    # Your code here - create a complex query using Q objects
    # For example: Find all beginner courses that either:
    # - Have no prerequisites, or
    # - Are taught by instructors who joined before 2023
    pass
```

## Exercise 3: Model Methods and Properties

Add useful methods and properties to your models:

```python
# Add these to the appropriate models

# Course model
def get_enrolled_students(self):
    """Return a QuerySet of all enrolled students"""
    # Your code here
    pass
    
@property
def completion_rate(self):
    """Calculate the percentage of students who completed the course"""
    # Your code here
    pass

# Instructor model
def get_total_students(self):
    """Return the total number of students across all courses"""
    # Your code here
    pass
    
@property
def average_course_size(self):
    """Calculate the average number of students per course"""
    # Your code here
    pass

# Enrollment model
@property
def is_passing(self):
    """Return True if the student's grade is passing (>= 60)"""
    # Your code here
    pass
```

## Exercise 4: Custom Management Command

Create a management command to generate a report of course statistics:

```python
# Create courses/management/commands/generate_course_report.py

from django.core.management.base import BaseCommand
from courses.models import Course, Enrollment, Instructor
from django.db.models import Avg, Count, Sum, Q, F
import csv
import os

class Command(BaseCommand):
    help = 'Generate a CSV report of course statistics'
    
    def add_arguments(self, parser):
        parser.add_argument('--output', type=str, default='course_report.csv',
                            help='Output file name')
    
    def handle(self, *args, **options):
        # Your code here - generate a CSV report with:
        # - Course code and title
        # - Instructor name
        # - Number of students enrolled
        # - Average grade
        # - Completion rate
        # - Number of prerequisites
        pass
```

## Submission

To complete this exercise:

1. Implement all the tasks above
2. Run migrations to update your database schema
3. Add some sample data using the Django admin
4. Test your views and functionality
5. Submit your code along with screenshots of:
   - The admin interface for your new models
   - The assignment list and detail views
   - The submission form
   - The CSV report generated by your management command