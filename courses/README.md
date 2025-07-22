# Session 7: Models, ORM, and Admin

This directory contains the implementation for Session 7 of the course, focusing on Django models, ORM, and Admin customization.

## Features Implemented

### 1. Django Models with Various Field Types

- **Instructor Model**: OneToOneField relationship with User, TextField, CharField, ImageField, DateField
- **Course Model**: CharField, TextField, PositiveSmallIntegerField, ForeignKey, ManyToManyField, DateField, BooleanField
- **Enrollment Model**: ForeignKey relationships, DateField, CharField with choices

### 2. Model Relationships

- **OneToOne**: Instructor to User
- **ForeignKey (Many-to-One)**: Course to Instructor, Enrollment to Course and User
- **ManyToMany**: Course prerequisites (self-referential)

### 3. Django Admin Customization

- Custom list displays and filters
- Search functionality
- Custom methods for display
- Fieldsets for organizing admin forms
- Horizontal filters for ManyToMany fields
- Date hierarchies

### 4. Data Seeding

- Management command for populating the database with sample data
- Creation of instructors, courses, and student enrollments
- Setting up relationships between models

## How to Use

### Running the Application

```bash
# Start the development server
python manage.py runserver

# Access the course management system
http://127.0.0.1:8000/courses/
```

### Admin Access

```
URL: http://127.0.0.1:8000/admin/
Username: admin
Password: adminpassword
```

### Sample User Accounts

**Instructors:**
- Username: jsmith, Password: jsmith123
- Username: mjohnson, Password: mjohnson123
- Username: alee, Password: alee123

**Students:**
- Username: student1, Password: student1123
- Username: student2, Password: student2123
- Username: student3, Password: student3123
- Username: student4, Password: student4123
- Username: student5, Password: student5123

## Key Learning Points

1. **Model Design**: Creating models with appropriate fields and relationships
2. **Migrations**: Managing database schema changes
3. **ORM Usage**: Querying and filtering data using Django's ORM
4. **Admin Customization**: Enhancing the admin interface for better usability
5. **Data Management**: Seeding and maintaining relational data

## Exercises

1. Add a new field to the Course model for "syllabus" (FileField)
2. Create a new model for "Assignment" with ForeignKey to Course
3. Customize the admin interface for the new Assignment model
4. Add a view to display assignments for a specific course
5. Implement a form for instructors to create new assignments