"""SQLite Tutorial: Introduction and SQL Basics (CRUD)

This script demonstrates the basics of SQLite operations including:
1. Creating a database and tables
2. Inserting, reading, updating, and deleting data (CRUD)
3. Using parameterized queries
4. Working with context managers
5. Query optimization with EXPLAIN

Follow along with the comments to understand each step.
"""

import sqlite3
import os
import csv
from datetime import datetime
from pathlib import Path

# Get the current directory where this script is located
BASE_DIR = Path(__file__).resolve().parent

# Database file path
DB_PATH = BASE_DIR / 'student_database.sqlite'

# CSV file path
CSV_PATH = BASE_DIR / 'students.csv'

# Check if database already exists and remove it for fresh start
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
    print(f"Removed existing database at {DB_PATH}")

# Part 1: Creating a database and table
# =====================================

# Connect to the SQLite database (creates it if it doesn't exist)
conn = sqlite3.connect(DB_PATH)
print(f"Connected to database at {DB_PATH}")

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create a students table
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
print("Created students table")

# Commit the changes and close the connection
conn.commit()
conn.close()

# Part 2: CRUD Operations - Create (Insert)
# ========================================

# Using context manager (with statement) for better resource management
with sqlite3.connect(DB_PATH) as conn:
    cursor = conn.cursor()
    
    # Read data from CSV file
    with open(CSV_PATH, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        # Insert each row into the database using parameterized queries
        for row in csv_reader:
            # Using parameterized query for security (prevents SQL injection)
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

# Part 3: CRUD Operations - Read (Select)
# ======================================

with sqlite3.connect(DB_PATH) as conn:
    # Configure connection to return rows as dictionaries
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print("\n--- All Students ---")
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    
    for student in students:
        # Access by column name since we're using sqlite3.Row
        print(f"ID: {student['id']}, Name: {student['first_name']} {student['last_name']}, Major: {student['major']}, GPA: {student['gpa']}")
    
    print("\n--- Students with GPA > 3.5 ---")
    # Parameterized query with filtering
    cursor.execute("SELECT * FROM students WHERE gpa > ?", (3.5,))
    high_gpa_students = cursor.fetchall()
    
    for student in high_gpa_students:
        print(f"ID: {student['id']}, Name: {student['first_name']} {student['last_name']}, GPA: {student['gpa']}")
    
    print("\n--- Computer Science Students ---")
    # Using LIKE for pattern matching
    cursor.execute("SELECT * FROM students WHERE major LIKE ?", ('Computer Science',))
    cs_students = cursor.fetchall()
    
    for student in cs_students:
        print(f"ID: {student['id']}, Name: {student['first_name']} {student['last_name']}, Email: {student['email']}")

# Part 4: CRUD Operations - Update
# ===============================

with sqlite3.connect(DB_PATH) as conn:
    cursor = conn.cursor()
    
    # Update a student's GPA
    cursor.execute('''
    UPDATE students
    SET gpa = ?
    WHERE id = ?
    ''', (4.0, 1))
    
    print(f"\nUpdated GPA for student with ID 1. Rows affected: {cursor.rowcount}")
    
    # Verify the update
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id = 1")
    student = cursor.fetchone()
    print(f"Updated student: ID: {student['id']}, Name: {student['first_name']} {student['last_name']}, GPA: {student['gpa']}")

# Part 5: CRUD Operations - Delete
# ===============================

with sqlite3.connect(DB_PATH) as conn:
    cursor = conn.cursor()
    
    # Delete a student
    cursor.execute("DELETE FROM students WHERE id = ?", (15,))
    
    print(f"\nDeleted student with ID 15. Rows affected: {cursor.rowcount}")
    
    # Verify the deletion by counting remaining students
    cursor.execute("SELECT COUNT(*) FROM students")
    count = cursor.fetchone()[0]
    print(f"Remaining students in database: {count}")

# Part 6: Query Optimization with EXPLAIN
# =====================================

with sqlite3.connect(DB_PATH) as conn:
    cursor = conn.cursor()
    
    print("\n--- Query Execution Plan ---")
    # EXPLAIN QUERY PLAN shows how SQLite will execute the query
    cursor.execute("EXPLAIN QUERY PLAN SELECT * FROM students WHERE major = 'Computer Science'")
    plan = cursor.fetchall()
    for row in plan:
        print(f"Step {row[0]}: {row[3]}")
    
    # Create an index to optimize queries on the major field
    print("\nCreating index on major field...")
    cursor.execute("CREATE INDEX idx_major ON students(major)")
    
    # Check the execution plan again after creating the index
    print("\n--- Query Execution Plan After Index Creation ---")
    cursor.execute("EXPLAIN QUERY PLAN SELECT * FROM students WHERE major = 'Computer Science'")
    plan = cursor.fetchall()
    for row in plan:
        print(f"Step {row[0]}: {row[3]}")

# Part 7: Advanced Queries
# ======================

with sqlite3.connect(DB_PATH) as conn:
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print("\n--- Student Statistics ---")
    cursor.execute('''
    SELECT 
        major, 
        COUNT(*) as student_count, 
        AVG(gpa) as average_gpa,
        MIN(gpa) as min_gpa,
        MAX(gpa) as max_gpa
    FROM students
    GROUP BY major
    ORDER BY average_gpa DESC
    ''')
    
    stats = cursor.fetchall()
    print(f"{'Major':<20} {'Count':<10} {'Avg GPA':<10} {'Min GPA':<10} {'Max GPA':<10}")
    print("-" * 60)
    for row in stats:
        print(f"{row['major']:<20} {row['student_count']:<10} {row['average_gpa']:.2f}{' ':<6} {row['min_gpa']:.2f}{' ':<6} {row['max_gpa']:.2f}")

print("\nSQLite tutorial completed successfully!")