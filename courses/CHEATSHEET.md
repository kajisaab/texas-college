# Django Models & ORM Cheat Sheet

## Model Definition

```python
from django.db import models
from django.contrib.auth.models import User

class MyModel(models.Model):
    # Field types
    char_field = models.CharField(max_length=100)
    text_field = models.TextField()
    integer_field = models.IntegerField()
    positive_integer = models.PositiveIntegerField()
    float_field = models.FloatField()
    decimal_field = models.DecimalField(max_digits=10, decimal_places=2)
    boolean_field = models.BooleanField(default=True)
    date_field = models.DateField(auto_now_add=True)  # Set on creation
    datetime_field = models.DateTimeField(auto_now=True)  # Updated on save
    email_field = models.EmailField()
    url_field = models.URLField()
    file_field = models.FileField(upload_to='files/')
    image_field = models.ImageField(upload_to='images/')
    json_field = models.JSONField()
    
    # Field options
    nullable = models.CharField(max_length=100, null=True)  # Allow NULL in database
    blankable = models.CharField(max_length=100, blank=True)  # Allow blank in forms
    unique_field = models.CharField(max_length=100, unique=True)
    indexed_field = models.CharField(max_length=100, db_index=True)
    with_default = models.IntegerField(default=0)
    with_choices = models.CharField(
        max_length=3,
        choices=[
            ('OPT', 'Option One'),
            ('TWT', 'Option Two'),
        ],
        default='OPT'
    )
    with_help = models.CharField(max_length=100, help_text="Help text for forms")
    
    # Relationships
    foreign_key = models.ForeignKey(
        'AnotherModel',
        on_delete=models.CASCADE,  # CASCADE, PROTECT, SET_NULL, SET_DEFAULT, DO_NOTHING
        related_name='related_objects',  # Name for reverse relation
        null=True,
        blank=True
    )
    many_to_many = models.ManyToManyField(
        'AnotherModel',
        related_name='m2m_related',
        blank=True
    )
    one_to_one = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    
    # Meta options
    class Meta:
        verbose_name = 'My Model'
        verbose_name_plural = 'My Models'
        ordering = ['-date_field', 'char_field']  # Default ordering
        unique_together = [['field1', 'field2']]  # Composite unique constraint
        indexes = [models.Index(fields=['field1', 'field2'])]  # Composite index
        abstract = False  # If True, this model will be abstract
        db_table = 'custom_table_name'  # Custom database table name
    
    # String representation
    def __str__(self):
        return self.char_field
    
    # Custom methods
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('model-detail', kwargs={'pk': self.pk})
    
    # Custom properties
    @property
    def calculated_value(self):
        return self.integer_field * 2
```

## Migrations

```bash
# Create migrations
python manage.py makemigrations [app_name]

# Apply migrations
python manage.py migrate [app_name]

# Show migration status
python manage.py showmigrations [app_name]

# Show SQL for migration
python manage.py sqlmigrate app_name migration_name
```

## ORM Queries

### Creating Objects

```python
# Method 1: Create and save
obj = MyModel(char_field='value', integer_field=42)
obj.save()

# Method 2: Create with one call
obj = MyModel.objects.create(char_field='value', integer_field=42)

# Method 3: Get or create
obj, created = MyModel.objects.get_or_create(
    char_field='value',
    defaults={'integer_field': 42}  # Used only when creating
)

# Method 4: Update or create
obj, created = MyModel.objects.update_or_create(
    char_field='value',  # Lookup parameters
    defaults={'integer_field': 42}  # Update parameters
)

# Bulk create
MyModel.objects.bulk_create([
    MyModel(char_field='value1'),
    MyModel(char_field='value2'),
])
```

### Retrieving Objects

```python
# Get all objects
all_objects = MyModel.objects.all()

# Get specific object (raises DoesNotExist if not found)
obj = MyModel.objects.get(id=1)

# Get first object (returns None if not found)
obj = MyModel.objects.filter(char_field='value').first()

# Get last object
obj = MyModel.objects.order_by('-id').first()

# Filter objects
filtered = MyModel.objects.filter(integer_field__gt=10)

# Exclude objects
excluded = MyModel.objects.exclude(char_field='value')

# Limit results
limited = MyModel.objects.all()[:5]  # First 5
offset = MyModel.objects.all()[5:10]  # 5 to 10

# Order results
ordered = MyModel.objects.order_by('char_field', '-integer_field')

# Count objects
count = MyModel.objects.filter(boolean_field=True).count()

# Check if exists
exists = MyModel.objects.filter(id=1).exists()
```

### Field Lookups

```python
# Exact match (default)
MyModel.objects.filter(char_field='value')

# Case-insensitive exact match
MyModel.objects.filter(char_field__iexact='VALUE')

# Contains
MyModel.objects.filter(char_field__contains='alu')
MyModel.objects.filter(char_field__icontains='ALU')  # Case-insensitive

# Starts/ends with
MyModel.objects.filter(char_field__startswith='val')
MyModel.objects.filter(char_field__endswith='lue')

# Numeric comparisons
MyModel.objects.filter(integer_field__gt=10)  # Greater than
MyModel.objects.filter(integer_field__gte=10)  # Greater than or equal
MyModel.objects.filter(integer_field__lt=10)  # Less than
MyModel.objects.filter(integer_field__lte=10)  # Less than or equal

# Range
MyModel.objects.filter(integer_field__range=(10, 20))

# Date lookups
from datetime import date
MyModel.objects.filter(date_field__year=2023)
MyModel.objects.filter(date_field__month=12)
MyModel.objects.filter(date_field__day=25)
MyModel.objects.filter(date_field__week_day=1)  # Sunday=1, Saturday=7
MyModel.objects.filter(date_field__range=(date(2023, 1, 1), date(2023, 12, 31)))

# NULL checks
MyModel.objects.filter(nullable__isnull=True)
MyModel.objects.filter(nullable__isnull=False)

# Multiple values (IN)
MyModel.objects.filter(id__in=[1, 2, 3])
```

### Complex Queries

```python
# Q objects for OR conditions
from django.db.models import Q
MyModel.objects.filter(Q(char_field='value1') | Q(char_field='value2'))

# AND conditions
MyModel.objects.filter(Q(char_field='value') & Q(integer_field__gt=10))

# NOT condition
MyModel.objects.filter(~Q(char_field='value'))

# Complex combinations
MyModel.objects.filter(
    (Q(char_field='value1') | Q(char_field='value2')) &
    Q(integer_field__gt=10)
)
```

### Aggregation and Annotation

```python
# Aggregation
from django.db.models import Avg, Count, Max, Min, Sum

# Single aggregation
avg_value = MyModel.objects.aggregate(Avg('integer_field'))

# Multiple aggregations
stats = MyModel.objects.aggregate(
    avg_value=Avg('integer_field'),
    max_value=Max('integer_field'),
    total=Sum('integer_field'),
    count=Count('id')
)

# Annotation (adds calculated field to each object)
annotated = MyModel.objects.annotate(
    related_count=Count('foreign_key'),
    doubled_value=F('integer_field') * 2
)

# Group by with annotation
from django.db.models import F
group_counts = MyModel.objects.values('char_field').annotate(
    count=Count('id'),
    avg_value=Avg('integer_field')
).order_by('-count')
```

### Relationships

```python
# Forward relationship (ForeignKey)
related_objects = MyModel.objects.filter(foreign_key__char_field='value')

# Reverse relationship
parent_model = AnotherModel.objects.get(id=1)
related_objects = parent_model.related_objects.all()  # Using related_name

# Many-to-many relationships
obj = MyModel.objects.get(id=1)
related_m2m = obj.many_to_many.all()

# Add to many-to-many
obj.many_to_many.add(another_obj)
obj.many_to_many.add(another_obj1, another_obj2)

# Remove from many-to-many
obj.many_to_many.remove(another_obj)

# Clear all many-to-many relationships
obj.many_to_many.clear()

# Set specific many-to-many relationships
obj.many_to_many.set([another_obj1, another_obj2])
```

### Performance Optimization

```python
# Select related (for ForeignKey and OneToOneField)
obj = MyModel.objects.select_related('foreign_key').get(id=1)

# Prefetch related (for reverse ForeignKey and ManyToManyField)
objs = MyModel.objects.prefetch_related('many_to_many').all()

# Combining both
objs = MyModel.objects.select_related('foreign_key').prefetch_related('many_to_many')

# Only retrieve specific fields
objs = MyModel.objects.only('id', 'char_field')

# Defer specific fields (retrieve all except these)
objs = MyModel.objects.defer('text_field')

# Count with optimization
count = MyModel.objects.filter(boolean_field=True).count()

# Exists for checking existence efficiently
if MyModel.objects.filter(id=1).exists():
    # Do something
```

### Updating Objects

```python
# Update single object
obj = MyModel.objects.get(id=1)
obj.char_field = 'new value'
obj.save()

# Update specific fields
obj.save(update_fields=['char_field'])

# Bulk update
MyModel.objects.filter(boolean_field=True).update(integer_field=F('integer_field') + 1)

# F expressions for field-based updates
from django.db.models import F
MyModel.objects.update(integer_field=F('integer_field') * 2)
```

### Deleting Objects

```python
# Delete single object
obj = MyModel.objects.get(id=1)
obj.delete()

# Bulk delete
MyModel.objects.filter(boolean_field=False).delete()

# Delete all
MyModel.objects.all().delete()
```

## Admin Customization

```python
from django.contrib import admin
from .models import MyModel

# Basic registration
admin.site.register(MyModel)

# Custom admin class
@admin.register(MyModel)
class MyModelAdmin(admin.ModelAdmin):
    # Display options
    list_display = ('id', 'char_field', 'integer_field', 'calculated_display')
    list_display_links = ('id', 'char_field')  # Clickable fields
    list_editable = ('integer_field',)  # Editable in list view
    list_filter = ('boolean_field', 'with_choices')  # Filters in sidebar
    list_per_page = 25  # Pagination
    search_fields = ('char_field', 'text_field')  # Searchable fields
    date_hierarchy = 'date_field'  # Date-based drilldown
    
    # Detail view options
    fieldsets = (
        ('Basic Information', {
            'fields': ('char_field', 'text_field'),
            'description': 'Basic fields for the model'
        }),
        ('Advanced', {
            'fields': ('integer_field', 'boolean_field'),
            'classes': ('collapse',)  # Collapsible section
        }),
    )
    readonly_fields = ('date_field',)  # Non-editable fields
    
    # Many-to-many display options
    filter_horizontal = ('many_to_many',)  # Horizontal filter
    # OR filter_vertical = ('many_to_many',)  # Vertical filter
    
    # Inline related objects
    inlines = [RelatedModelInline]
    
    # Custom display method
    def calculated_display(self, obj):
        return obj.integer_field * 2
    calculated_display.short_description = 'Calculated Value'
    calculated_display.admin_order_field = 'integer_field'  # Sortable
    
    # Custom actions
    actions = ['make_active', 'make_inactive']
    
    def make_active(self, request, queryset):
        queryset.update(boolean_field=True)
    make_active.short_description = 'Mark selected as active'
    
    def make_inactive(self, request, queryset):
        queryset.update(boolean_field=False)
    make_inactive.short_description = 'Mark selected as inactive'

# Inline admin for related models
class RelatedModelInline(admin.TabularInline):  # or StackedInline
    model = RelatedModel
    extra = 1  # Number of empty forms
    min_num = 0  # Minimum number of forms
    max_num = 10  # Maximum number of forms
```