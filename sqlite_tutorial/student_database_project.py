"""Student Database Project

This hands-on project demonstrates:
1. Building a student database from CSV data
2. Generating various reports using SQL queries
3. Applying best practices for SQLite in Python
"""

import sqlite3
import csv
import os
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

# Get the current directory where this script is located
BASE_DIR = Path(__file__).resolve().parent

# Database file path
DB_PATH = BASE_DIR / 'student_project.sqlite'

# CSV file path
CSV_PATH = BASE_DIR / 'students.csv'

# Reports directory
REPORTS_DIR = BASE_DIR / 'reports'
os.makedirs(REPORTS_DIR, exist_ok=True)

# Create a database connection with row factory
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn

# Initialize the database
def initialize_database():
    # Remove existing database for fresh start
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"Removed existing database at {DB_PATH}")
    
    # Create a new database and tables
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        
        # Create students table
        cursor.execute('''
        CREATE TABLE students (
            id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            major TEXT NOT NULL,
            gpa REAL NOT NULL,
            enrollment_date TEXT NOT NULL
        )
        ''')
        
        # Create courses table
        cursor.execute('''
        CREATE TABLE courses (
            id INTEGER PRIMARY KEY,
            course_code TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            credits INTEGER NOT NULL,
            department TEXT NOT NULL
        )
        ''')
        
        # Create enrollments table (many-to-many relationship)
        cursor.execute('''
        CREATE TABLE enrollments (
            id INTEGER PRIMARY KEY,
            student_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            semester TEXT NOT NULL,
            grade TEXT,
            FOREIGN KEY (student_id) REFERENCES students (id),
            FOREIGN KEY (course_id) REFERENCES courses (id),
            UNIQUE (student_id, course_id, semester)
        )
        ''')
        
        print("Database initialized with tables: students, courses, enrollments")

# Import student data from CSV
def import_students_from_csv():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Read data from CSV file
        with open(CSV_PATH, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            
            # Insert each row into the database
            for row in csv_reader:
                cursor.execute('''
                INSERT INTO students (id, first_name, last_name, email, major, gpa, enrollment_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    row['id'],
                    row['first_name'],
                    row['last_name'],
                    row['email'],
                    row['major'],
                    row['gpa'],
                    row['enrollment_date']
                ))
        
        print(f"Imported {cursor.rowcount if hasattr(cursor, 'rowcount') else '15'} students from CSV")

# Add sample courses
def add_sample_courses():
    courses = [
        ("CS101", "Introduction to Computer Science", 3, "Computer Science"),
        ("CS201", "Data Structures", 4, "Computer Science"),
        ("CS301", "Database Systems", 3, "Computer Science"),
        ("MATH101", "Calculus I", 4, "Mathematics"),
        ("MATH201", "Linear Algebra", 3, "Mathematics"),
        ("PHYS101", "Physics I", 4, "Physics"),
        ("BIO101", "Introduction to Biology", 3, "Biology"),
        ("CHEM101", "General Chemistry", 4, "Chemistry"),
        ("ENG101", "English Composition", 3, "English"),
        ("HIST101", "World History", 3, "History")
    ]
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        for i, (code, title, credits, department) in enumerate(courses, 1):
            cursor.execute('''
            INSERT INTO courses (id, course_code, title, credits, department)
            VALUES (?, ?, ?, ?, ?)
            ''', (i, code, title, credits, department))
        
        print(f"Added {len(courses)} sample courses")

# Generate random enrollments
def generate_enrollments():
    import random
    
    # Get all student IDs
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM students")
        student_ids = [row['id'] for row in cursor.fetchall()]
        
        # Get all course IDs
        cursor.execute("SELECT id FROM courses")
        course_ids = [row['id'] for row in cursor.fetchall()]
        
        # Semesters
        semesters = ["Fall 2022", "Spring 2023", "Fall 2023"]
        
        # Possible grades
        grades = ["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "F", None]  # None for in-progress
        
        # Generate enrollments
        enrollments = []
        enrollment_id = 1
        
        for student_id in student_ids:
            # Each student takes 3-6 random courses
            num_courses = random.randint(3, 6)
            selected_courses = random.sample(course_ids, num_courses)
            
            for course_id in selected_courses:
                # Assign a random semester
                semester = random.choice(semesters)
                
                # Assign a grade (or None for in-progress)
                grade = random.choice(grades)
                
                enrollments.append((enrollment_id, student_id, course_id, semester, grade))
                enrollment_id += 1
        
        # Insert enrollments
        for enrollment in enrollments:
            try:
                cursor.execute('''
                INSERT INTO enrollments (id, student_id, course_id, semester, grade)
                VALUES (?, ?, ?, ?, ?)
                ''', enrollment)
            except sqlite3.IntegrityError:
                # Skip duplicate enrollments
                pass
        
        print(f"Generated {cursor.rowcount if hasattr(cursor, 'rowcount') else len(enrollments)} student enrollments")

# Generate reports
def generate_reports():
    with get_db_connection() as conn:
        # Report 1: Students by Major
        print("\nGenerating Report: Students by Major")
        cursor = conn.cursor()
        cursor.execute('''
        SELECT major, COUNT(*) as count
        FROM students
        GROUP BY major
        ORDER BY count DESC
        ''')
        
        results = cursor.fetchall()
        
        # Save to CSV
        with open(REPORTS_DIR / 'students_by_major.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Major', 'Count'])
            for row in results:
                writer.writerow([row['major'], row['count']])
        
        # Create visualization
        df = pd.DataFrame([(row['major'], row['count']) for row in results], columns=['Major', 'Count'])
        plt.figure(figsize=(10, 6))
        plt.bar(df['Major'], df['Count'])
        plt.title('Students by Major')
        plt.xlabel('Major')
        plt.ylabel('Number of Students')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(REPORTS_DIR / 'students_by_major.png')
        plt.close()
        
        # Report 2: GPA Distribution
        print("Generating Report: GPA Distribution")
        cursor.execute('''
        SELECT 
            CASE 
                WHEN gpa >= 3.7 THEN 'A (3.7-4.0)'
                WHEN gpa >= 3.3 THEN 'B+ (3.3-3.7)'
                WHEN gpa >= 3.0 THEN 'B (3.0-3.3)'
                WHEN gpa >= 2.7 THEN 'B- (2.7-3.0)'
                WHEN gpa >= 2.3 THEN 'C+ (2.3-2.7)'
                WHEN gpa >= 2.0 THEN 'C (2.0-2.3)'
                ELSE 'Below C (< 2.0)'
            END as gpa_range,
            COUNT(*) as count
        FROM students
        GROUP BY gpa_range
        ORDER BY MIN(gpa) DESC
        ''')
        
        results = cursor.fetchall()
        
        # Save to CSV
        with open(REPORTS_DIR / 'gpa_distribution.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['GPA Range', 'Count'])
            for row in results:
                writer.writerow([row['gpa_range'], row['count']])
        
        # Create visualization
        df = pd.DataFrame([(row['gpa_range'], row['count']) for row in results], columns=['GPA Range', 'Count'])
        plt.figure(figsize=(10, 6))
        plt.bar(df['GPA Range'], df['Count'])
        plt.title('GPA Distribution')
        plt.xlabel('GPA Range')
        plt.ylabel('Number of Students')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(REPORTS_DIR / 'gpa_distribution.png')
        plt.close()
        
        # Report 3: Course Enrollment Statistics
        print("Generating Report: Course Enrollment Statistics")
        cursor.execute('''
        SELECT 
            c.course_code,
            c.title,
            COUNT(e.id) as enrollment_count,
            AVG(s.gpa) as avg_student_gpa
        FROM courses c
        LEFT JOIN enrollments e ON c.id = e.course_id
        LEFT JOIN students s ON e.student_id = s.id
        GROUP BY c.id
        ORDER BY enrollment_count DESC
        ''')
        
        results = cursor.fetchall()
        
        # Save to CSV
        with open(REPORTS_DIR / 'course_enrollments.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Course Code', 'Title', 'Enrollment Count', 'Average Student GPA'])
            for row in results:
                writer.writerow([row['course_code'], row['title'], row['enrollment_count'], 
                                row['avg_student_gpa'] if row['avg_student_gpa'] else 'N/A'])
        
        # Report 4: Student Performance Report
        print("Generating Report: Student Performance Report")
        cursor.execute('''
        SELECT 
            s.id,
            s.first_name || ' ' || s.last_name as student_name,
            s.major,
            s.gpa as overall_gpa,
            COUNT(e.id) as courses_taken,
            SUM(CASE WHEN e.grade IS NOT NULL THEN 1 ELSE 0 END) as courses_completed,
            SUM(CASE WHEN e.grade IN ('A', 'A-') THEN 1 ELSE 0 END) as a_grades,
            SUM(CASE WHEN e.grade IN ('B+', 'B', 'B-') THEN 1 ELSE 0 END) as b_grades,
            SUM(CASE WHEN e.grade IN ('C+', 'C', 'C-') THEN 1 ELSE 0 END) as c_grades,
            SUM(CASE WHEN e.grade IN ('D+', 'D') THEN 1 ELSE 0 END) as d_grades,
            SUM(CASE WHEN e.grade = 'F' THEN 1 ELSE 0 END) as f_grades
        FROM students s
        LEFT JOIN enrollments e ON s.id = e.student_id
        GROUP BY s.id
        ORDER BY overall_gpa DESC
        ''')
        
        results = cursor.fetchall()
        
        # Save to CSV
        with open(REPORTS_DIR / 'student_performance.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Student Name', 'Major', 'Overall GPA', 'Courses Taken', 
                           'Courses Completed', 'A Grades', 'B Grades', 'C Grades', 'D Grades', 'F Grades'])
            for row in results:
                writer.writerow([row['id'], row['student_name'], row['major'], row['overall_gpa'],
                               row['courses_taken'], row['courses_completed'], row['a_grades'],
                               row['b_grades'], row['c_grades'], row['d_grades'], row['f_grades']])
        
        print(f"All reports generated and saved to {REPORTS_DIR}")

# Main function to run the project
def main():
    print("Student Database Project")
    print("=======================\n")
    
    # Initialize the database
    initialize_database()
    
    # Import student data
    import_students_from_csv()
    
    # Add sample courses
    add_sample_courses()
    
    # Generate enrollments
    generate_enrollments()
    
    # Generate reports
    generate_reports()
    
    print("\nProject completed successfully!")
    print(f"Database file: {DB_PATH}")
    print(f"Reports directory: {REPORTS_DIR}")

# Run the project
if __name__ == "__main__":
    main()