# Session 7: Django Models, ORM, and Admin Guide

## Overview

This guide provides a comprehensive overview of the Course Management System implemented for Session 7. The system demonstrates Django's powerful Model-View-Template (MVT) architecture with a focus on models, the Object-Relational Mapping (ORM) system, and Admin interface customization.

## Project Structure

```
courses/
├── admin.py          # Admin interface customization
├── models.py         # Database models definition
├── views.py          # View functions for handling requests
├── urls.py           # URL routing configuration
├── templates/        # HTML templates
│   └── courses/
│       ├── base.html
│       ├── course_list.html
│       ├── course_detail.html
│       ├── instructor_detail.html
│       └── my_courses.html
└── management/       # Custom management commands
    └── commands/
        └── seed_courses.py  # Data seeding command
```

## Models

The application includes three main models:

### Instructor Model

```python
class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    expertise = models.CharField(max_length=255, blank=True)
    office_hours = models.CharField(max_length=255, blank=True)
    profile_picture = models.ImageField(upload_to='instructor_profiles/', blank=True, null=True)
    join_date = models.DateField(auto_now_add=True)
```

### Course Model

```python
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
    instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL, null=True, related_name='courses')
    level = models.CharField(max_length=3, choices=LEVEL_CHOICES, default='BEG')
    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
```

### Enrollment Model

```python
class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('ACT', 'Active'),
        ('CMP', 'Completed'),
        ('DRP', 'Dropped'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default='ACT')
    grade = models.PositiveSmallIntegerField(null=True, blank=True)
```

## Key Features

### 1. Model Relationships

The system demonstrates three types of relationships:

- **One-to-One**: Instructor to User
- **Many-to-One (ForeignKey)**: Course to Instructor, Enrollment to Course and User
- **Many-to-Many**: Course prerequisites (self-referential)

### 2. Admin Customization

The admin interface is customized for better usability:

```python
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'instructor_name', 'level', 'credits', 'is_active')
    list_filter = ('level', 'is_active', 'start_date')
    search_fields = ('code', 'title', 'description')
    filter_horizontal = ('prerequisites',)
    date_hierarchy = 'start_date'
    
    fieldsets = (
        ('Course Information', {
            'fields': ('title', 'code', 'description', 'credits', 'level')
        }),
        ('Instructor and Prerequisites', {
            'fields': ('instructor', 'prerequisites')
        }),
        ('Schedule', {
            'fields': ('start_date', 'end_date', 'is_active')
        }),
    )
```

### 3. Data Seeding

A custom management command (`seed_courses`) populates the database with sample data:

```python
python manage.py seed_courses
```

This creates:
- Admin user
- Instructors with profiles
- Courses with prerequisites
- Student accounts
- Enrollments with random statuses and grades

### 4. Views and Templates

The application includes views for:

- Course listing with search and filtering
- Course details with prerequisite checking
- Instructor profiles
- User-specific course listings

## ORM Usage Examples

### Basic Queries

```python
# Get all active courses
active_courses = Course.objects.filter(is_active=True)

# Get courses taught by a specific instructor
instructor_courses = Course.objects.filter(instructor__user__username='jsmith')

# Get a specific course with its instructor (using select_related for optimization)
course = Course.objects.select_related('instructor').get(code='CS101')
```

### Complex Queries

```python
# Get courses with their enrollment counts
from django.db.models import Count
courses_with_counts = Course.objects.annotate(student_count=Count('enrollments'))

# Get courses that have no prerequisites
courses_no_prereqs = Course.objects.filter(prerequisites__isnull=True)

# Get all beginner courses that are active and have at least 5 students
from django.db.models import Q
popular_beginner_courses = Course.objects.filter(
    Q(level='BEG') & Q(is_active=True)
).annotate(
    student_count=Count('enrollments')
).filter(student_count__gte=5)
```

## Running the Application

1. Ensure all dependencies are installed:
   ```
   pip install Pillow  # Required for ImageField
   ```

2. Apply migrations:
   ```
   python manage.py makemigrations courses
   python manage.py migrate
   ```

3. Seed the database (optional):
   ```
   python manage.py seed_courses
   ```

4. Run the development server:
   ```
   python manage.py runserver
   ```

5. Access the application:
   - Course listing: http://127.0.0.1:8000/courses/
   - Admin interface: http://127.0.0.1:8000/admin/

## Learning Resources

- [Django Models Documentation](https://docs.djangoproject.com/en/5.2/topics/db/models/)
- [Django QuerySet API](https://docs.djangoproject.com/en/5.2/ref/models/querysets/)
- [Django Admin Customization](https://docs.djangoproject.com/en/5.2/ref/contrib/admin/)

## Next Steps

To extend this application, consider implementing:

1. Assignment and submission functionality
2. User profile management
3. Course rating and review system
4. API endpoints using Django REST Framework
5. Advanced reporting and analytics