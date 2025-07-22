#!/usr/bin/env python3
"""
Django Integration Script

This script demonstrates how to integrate SQLite operations with Django models.
It shows how to:
1. Import data from a CSV file into Django models
2. Query Django models using the ORM
3. Compare raw SQLite queries with Django ORM queries
"""

import os
import csv
import sys
import django
from datetime import datetime
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Add the project root to the Python path
sys.path.append(str(PROJECT_ROOT))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

# Import the StudentRecord model
from sqlite_tutorial.models import StudentRecord

# Get the current directory
BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / 'students.csv'

def import_students_from_csv():
    """Import students from CSV file into Django models"""
    # Clear existing students
    StudentRecord.objects.all().delete()
    print("Cleared existing students")
    
    # Read data from CSV file
    with open(CSV_PATH, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        # Insert each row into the database
        for row in csv_reader:
            StudentRecord.objects.create(
                first_name=row['first_name'],
                last_name=row['last_name'],
                email=row['email'],
                major=row['major'],
                gpa=float(row['gpa']),
                enrollment_date=datetime.strptime(row['enrollment_date'], '%Y-%m-%d').date()
            )
    
    print(f"Imported {StudentRecord.objects.count()} students from CSV")

def demonstrate_django_queries():
    """Demonstrate Django ORM queries"""
    print("\n--- Django ORM Queries ---")
    
    # Basic query - Get all students
    print("\n1. Get all students:")
    students = StudentRecord.objects.all()
    for student in students:
        print(f"ID: {student.id}, Name: {student.first_name} {student.last_name}, Major: {student.major}, GPA: {student.gpa}")
    
    # Filtering - Get students with GPA > 3.5
    print("\n2. Students with GPA > 3.5:")
    high_gpa_students = StudentRecord.objects.filter(gpa__gt=3.5)
    for student in high_gpa_students:
        print(f"ID: {student.id}, Name: {student.first_name} {student.last_name}, GPA: {student.gpa}")
    
    # Filtering with multiple conditions
    print("\n3. Computer Science students with GPA > 3.5:")
    cs_high_gpa = StudentRecord.objects.filter(major='Computer Science', gpa__gt=3.5)
    for student in cs_high_gpa:
        print(f"ID: {student.id}, Name: {student.first_name} {student.last_name}, GPA: {student.gpa}")
    
    # Ordering
    print("\n4. Students ordered by GPA (descending):")
    ordered_students = StudentRecord.objects.order_by('-gpa')
    for student in ordered_students[:5]:  # Top 5
        print(f"ID: {student.id}, Name: {student.first_name} {student.last_name}, GPA: {student.gpa}")
    
    # Aggregation
    from django.db.models import Avg, Count, Min, Max
    print("\n5. Aggregation - Average GPA by Major:")
    avg_gpa_by_major = StudentRecord.objects.values('major').annotate(
        count=Count('id'),
        avg_gpa=Avg('gpa'),
        min_gpa=Min('gpa'),
        max_gpa=Max('gpa')
    ).order_by('-avg_gpa')
    
    for major_stats in avg_gpa_by_major:
        print(f"Major: {major_stats['major']}")
        print(f"  Count: {major_stats['count']}")
        print(f"  Avg GPA: {major_stats['avg_gpa']:.2f}")
        print(f"  Min GPA: {major_stats['min_gpa']:.2f}")
        print(f"  Max GPA: {major_stats['max_gpa']:.2f}")

def compare_with_raw_sql():
    """Compare Django ORM queries with raw SQL"""
    print("\n--- Comparing Django ORM with Raw SQL ---")
    
    # Django ORM Query
    print("\n1. Django ORM - Students with GPA > 3.5:")
    orm_students = StudentRecord.objects.filter(gpa__gt=3.5).values('id', 'first_name', 'last_name', 'gpa')
    for student in orm_students:
        print(f"ID: {student['id']}, Name: {student['first_name']} {student['last_name']}, GPA: {student['gpa']}")
    
    # Equivalent Raw SQL Query
    print("\n2. Raw SQL - Students with GPA > 3.5:")
    raw_students = StudentRecord.objects.raw("SELECT id, first_name, last_name, gpa FROM student_records WHERE gpa > 3.5")
    for student in raw_students:
        print(f"ID: {student.id}, Name: {student.first_name} {student.last_name}, GPA: {student.gpa}")
    
    # Complex Query - Django ORM
    print("\n3. Django ORM - Complex Query:")
    orm_complex = StudentRecord.objects.filter(
        major__in=['Computer Science', 'Mathematics', 'Physics'],
        gpa__gte=3.5
    ).order_by('-gpa', 'last_name')
    
    for student in orm_complex:
        print(f"ID: {student.id}, Name: {student.first_name} {student.last_name}, Major: {student.major}, GPA: {student.gpa}")
    
    # Complex Query - Raw SQL
    print("\n4. Raw SQL - Complex Query:")
    raw_complex = StudentRecord.objects.raw("""
    SELECT id, first_name, last_name, major, gpa 
    FROM student_records 
    WHERE major IN ('Computer Science', 'Mathematics', 'Physics') 
    AND gpa >= 3.5 
    ORDER BY gpa DESC, last_name ASC
    """)
    
    for student in raw_complex:
        print(f"ID: {student.id}, Name: {student.first_name} {student.last_name}, Major: {student.major}, GPA: {student.gpa}")

def main():
    """Main function"""
    print("Django Integration with SQLite")
    print("=============================")
    
    # Check if we have students in the database
    if StudentRecord.objects.count() == 0:
        import_students_from_csv()
    else:
        print(f"Using existing {StudentRecord.objects.count()} students in database")
    
    # Demonstrate Django ORM queries
    demonstrate_django_queries()
    
    # Compare with raw SQL
    compare_with_raw_sql()
    
    print("\nDjango integration demonstration completed!")

if __name__ == "__main__":
    main()