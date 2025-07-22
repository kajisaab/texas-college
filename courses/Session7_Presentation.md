# Session 7: Models, ORM, and Admin

## Django Models

### What are Models?
- Python classes that define the structure of your database tables
- Each model maps to a single database table
- Each attribute represents a database field

### Field Types
- **CharField**: For small to medium-sized strings
- **TextField**: For unlimited text
- **IntegerField**, **FloatField**, **DecimalField**: For numeric data
- **BooleanField**: For true/false values
- **DateField**, **DateTimeField**: For dates and timestamps
- **EmailField**, **URLField**: For validated email addresses and URLs
- **FileField**, **ImageField**: For file uploads

### Field Options
- **null**: If True, Django will store empty values as NULL
- **blank**: If True, the field is allowed to be blank in forms
- **choices**: A list of tuples for limiting field values
- **default**: The default value for the field
- **help_text**: Additional text displayed in forms
- **unique**: If True, the field must be unique throughout the table
- **verbose_name**: A human-readable name for the field

## Relationships

### ForeignKey (Many-to-One)
```python
instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL, null=True)
```
- Links a record in one table to a single record in another table
- `on_delete` determines what happens when the referenced object is deleted
  - `CASCADE`: Delete the object containing the ForeignKey
  - `PROTECT`: Prevent deletion of the referenced object
  - `SET_NULL`: Set the ForeignKey to NULL
  - `SET_DEFAULT`: Set the ForeignKey to its default value

### ManyToManyField
```python
prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True)
```
- Links each record in one table to multiple records in another table
- Creates an intermediary table automatically
- `symmetrical=False` for self-referential relationships means A→B doesn't imply B→A

### OneToOneField
```python
user = models.OneToOneField(User, on_delete=models.CASCADE)
```
- Similar to ForeignKey but with a unique constraint
- Often used to extend existing models

## Migrations

### What are Migrations?
- Python files that describe changes to your database schema
- Generated based on changes to your models
- Applied to the database to update its structure

### Migration Commands
```bash
# Create migration files based on model changes
python manage.py makemigrations [app_name]

# Apply migrations to the database
python manage.py migrate [app_name]

# Show migration status
python manage.py showmigrations [app_name]

# Show SQL for a migration
python manage.py sqlmigrate app_name migration_name
```

## Django ORM

### Creating Objects
```python
# Method 1
course = Course(title="Python Programming", code="CS102")
course.save()

# Method 2
course = Course.objects.create(title="Python Programming", code="CS102")
```

### Retrieving Objects
```python
# Get all objects
courses = Course.objects.all()

# Get a single object
course = Course.objects.get(code="CS101")

# Filter objects
beginner_courses = Course.objects.filter(level="BEG")

# Exclude objects
non_beginner_courses = Course.objects.exclude(level="BEG")

# Order objects
sorted_courses = Course.objects.order_by('title')
```

### Complex Queries
```python
from django.db.models import Q, Count

# OR queries
courses = Course.objects.filter(Q(level="BEG") | Q(level="INT"))

# Annotations
courses = Course.objects.annotate(student_count=Count('enrollments'))

# Joins
courses = Course.objects.select_related('instructor')
enrollments = Enrollment.objects.select_related('student', 'course')
```

## Django Admin

### Basic Registration
```python
from django.contrib import admin
from .models import Course

admin.site.register(Course)
```

### Customized Registration
```python
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'instructor', 'is_active')
    list_filter = ('level', 'is_active')
    search_fields = ('code', 'title')
```

### Admin Features
- **list_display**: Fields to display in the list view
- **list_filter**: Fields to filter by in the sidebar
- **search_fields**: Fields to search in
- **list_editable**: Fields that can be edited from the list view
- **date_hierarchy**: Field to navigate by date
- **fieldsets**: Group fields in the detail view
- **filter_horizontal/filter_vertical**: Better interface for ManyToMany fields
- **readonly_fields**: Fields that cannot be edited
- **inlines**: Edit related objects in the same page

## Best Practices

1. **Model Design**
   - Keep models focused on a single responsibility
   - Use descriptive names for models and fields
   - Add `__str__` methods for readable representations

2. **Field Choices**
   - Use appropriate field types for the data
   - Set constraints (null, blank, unique) appropriately
   - Define choices as class constants

3. **Relationships**
   - Choose the right relationship type
   - Use `related_name` for reverse relationships
   - Consider `on_delete` behavior carefully

4. **Admin Customization**
   - Customize the admin for better usability
   - Use list_display, search_fields, and filters
   - Group fields logically with fieldsets

5. **Performance**
   - Use select_related() and prefetch_related() to optimize queries
   - Add indexes to fields frequently used in filters and ordering
   - Be mindful of query complexity