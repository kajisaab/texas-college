"""SQLite Tutorial: Parameterized Queries and Context Managers

This script demonstrates:
1. Using context managers with SQLite
2. Implementing parameterized queries for security
3. Avoiding SQL injection vulnerabilities
"""

import sqlite3
from pathlib import Path

# Get the database path
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / 'student_database.sqlite'

# Function to demonstrate SQL injection vulnerability
def unsafe_search(user_input):
    print(f"\n--- UNSAFE SEARCH (Vulnerable to SQL Injection) ---")
    print(f"Searching for: {user_input}")
    
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # UNSAFE: Directly inserting user input into SQL query
        query = f"SELECT * FROM students WHERE last_name = '{user_input}'" 
        print(f"Executing query: {query}")
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        print(f"Found {len(results)} results:")
        for row in results:
            print(f"ID: {row[0]}, Name: {row[1]} {row[2]}, Email: {row[3]}")
    
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    
    finally:
        # Always close connections
        cursor.close()
        conn.close()

# Function to demonstrate safe parameterized queries
def safe_search(user_input):
    print(f"\n--- SAFE SEARCH (Using Parameterized Queries) ---")
    print(f"Searching for: {user_input}")
    
    # Using context manager (with statement) for automatic resource cleanup
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            
            # SAFE: Using parameterized query with placeholder
            query = "SELECT * FROM students WHERE last_name = ?" 
            print(f"Executing query with parameter: {query}")
            
            cursor.execute(query, (user_input,))
            results = cursor.fetchall()
            
            print(f"Found {len(results)} results:")
            for row in results:
                print(f"ID: {row[0]}, Name: {row[1]} {row[2]}, Email: {row[3]}")
    
    except sqlite3.Error as e:
        print(f"Database error: {e}")

# Function to demonstrate multiple parameterized queries
def advanced_search(first_name=None, last_name=None, min_gpa=None):
    print(f"\n--- ADVANCED SEARCH (Multiple Parameters) ---")
    print(f"Searching for: First Name: {first_name}, Last Name: {last_name}, Min GPA: {min_gpa}")
    
    try:
        with sqlite3.connect(DB_PATH) as conn:
            # Configure connection to return rows as dictionaries
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Start with base query
            query = "SELECT * FROM students WHERE 1=1"
            params = []
            
            # Add conditions based on provided parameters
            if first_name:
                query += " AND first_name = ?"
                params.append(first_name)
            
            if last_name:
                query += " AND last_name = ?"
                params.append(last_name)
            
            if min_gpa is not None:
                query += " AND gpa >= ?"
                params.append(min_gpa)
            
            print(f"Executing query: {query}")
            print(f"With parameters: {params}")
            
            cursor.execute(query, params)
            results = cursor.fetchall()
            
            print(f"Found {len(results)} results:")
            for row in results:
                print(f"ID: {row['id']}, Name: {row['first_name']} {row['last_name']}, Major: {row['major']}, GPA: {row['gpa']}")
    
    except sqlite3.Error as e:
        print(f"Database error: {e}")

# Function to demonstrate transaction management with context managers
def transaction_example():
    print(f"\n--- TRANSACTION MANAGEMENT ---")
    
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            
            # Start a transaction block
            # Note: SQLite automatically starts a transaction when you execute the first query
            
            # Multiple operations that should be atomic (all succeed or all fail)
            print("Starting transaction with multiple operations...")
            
            # 1. Update GPA for Computer Science students
            cursor.execute("""
            UPDATE students 
            SET gpa = gpa * 1.1 
            WHERE major = ? AND gpa * 1.1 <= 4.0
            """, ('Computer Science',))
            cs_updates = cursor.rowcount
            
            # 2. Update GPA for Mathematics students
            cursor.execute("""
            UPDATE students 
            SET gpa = gpa * 1.05 
            WHERE major = ? AND gpa * 1.05 <= 4.0
            """, ('Mathematics',))
            math_updates = cursor.rowcount
            
            # The context manager will automatically commit if no exceptions occur
            print(f"Transaction completed successfully!")
            print(f"Updated {cs_updates} Computer Science students and {math_updates} Mathematics students")
            
            # Verify the updates
            cursor.execute("SELECT * FROM students WHERE major IN (?, ?)", ('Computer Science', 'Mathematics'))
            updated_students = cursor.fetchall()
            print(f"Updated student records: {len(updated_students)}")
    
    except sqlite3.Error as e:
        # The context manager will automatically rollback if an exception occurs
        print(f"Transaction failed and was rolled back. Error: {e}")

# Demonstrate SQL injection vulnerability
print("Demonstrating SQL injection vulnerability:")
print("1. Normal search:")
unsafe_search("Smith")

print("\n2. SQL Injection attack:")
# This malicious input will return all students regardless of last name
unsafe_search("' OR '1'='1")

# Demonstrate safe parameterized queries
print("\nDemonstrating safe parameterized queries:")
print("1. Normal search:")
safe_search("Smith")

print("\n2. Attempted SQL Injection attack (will not work):")
safe_search("' OR '1'='1")

# Demonstrate advanced parameterized queries
advanced_search(first_name="John", last_name="Doe")
advanced_search(min_gpa=3.5)
advanced_search(first_name="Jane", min_gpa=3.0)

# Demonstrate transaction management
transaction_example()

print("\nParameterized queries and context managers tutorial completed!")