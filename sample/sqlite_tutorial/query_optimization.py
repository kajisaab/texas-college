"""SQLite Tutorial: Query Optimization using EXPLAIN

This script demonstrates:
1. Using EXPLAIN to understand query execution plans
2. Creating and using indexes for query optimization
3. Measuring query performance improvements
"""

import sqlite3
import time
from pathlib import Path

# Get the database path
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / 'student_database.sqlite'

# Function to execute a query and measure its performance
def measure_query_performance(query, params=None, iterations=1000):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        
        # Warm up
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        cursor.fetchall()
        
        # Measure performance
        start_time = time.time()
        for _ in range(iterations):
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            cursor.fetchall()
        end_time = time.time()
        
        return (end_time - start_time) / iterations

# Function to explain a query execution plan
def explain_query(query, params=None):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        
        # Get the execution plan
        explain_query = f"EXPLAIN QUERY PLAN {query}"
        if params:
            cursor.execute(explain_query, params)
        else:
            cursor.execute(explain_query)
        
        plan = cursor.fetchall()
        return plan

# Function to create an index
def create_index(index_name, table, columns):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        
        # Check if index already exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name=?", (index_name,))
        if cursor.fetchone():
            print(f"Index {index_name} already exists")
            return False
        
        # Create the index
        columns_str = ", ".join(columns) if isinstance(columns, list) else columns
        cursor.execute(f"CREATE INDEX {index_name} ON {table}({columns_str})")
        print(f"Created index {index_name} on {table}({columns_str})")
        return True

# Function to drop an index
def drop_index(index_name):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(f"DROP INDEX IF EXISTS {index_name}")
        print(f"Dropped index {index_name}")

# Function to display table schema
def show_table_schema(table_name):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        print(f"\nSchema for table '{table_name}':")
        print(f"{'ID':<3} {'Name':<15} {'Type':<10} {'NotNull':<8} {'Default':<10} {'PK':<3}")
        print("-" * 50)
        for col in columns:
            print(f"{col[0]:<3} {col[1]:<15} {col[2]:<10} {col[3]:<8} {col[4] if col[4] is not None else 'NULL':<10} {col[5]:<3}")

# Function to show all indexes for a table
def show_indexes(table_name):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA index_list({table_name})")
        indexes = cursor.fetchall()
        
        print(f"\nIndexes for table '{table_name}':")
        if not indexes:
            print("No indexes found")
            return
        
        print(f"{'Seq':<5} {'Name':<20} {'Unique':<8}")
        print("-" * 35)
        for idx in indexes:
            print(f"{idx[0]:<5} {idx[1]:<20} {'Yes' if idx[2] else 'No':<8}")
            
            # Show the columns in this index
            cursor.execute(f"PRAGMA index_info({idx[1]})")
            index_columns = cursor.fetchall()
            print(f"  Columns: ", end="")
            for i, col_info in enumerate(index_columns):
                if i > 0:
                    print(", ", end="")
                print(f"{col_info[2]}", end="")
            print()

# Main demonstration
print("SQLite Query Optimization Tutorial")
print("=================================\n")

# Show the current schema
show_table_schema("students")

# Show existing indexes
show_indexes("students")

# Define test queries
queries = [
    {
        "name": "Query by Major",
        "sql": "SELECT * FROM students WHERE major = ?",
        "params": ("Computer Science",),
        "index_name": "idx_students_major",
        "index_columns": "major"
    },
    {
        "name": "Query by GPA Range",
        "sql": "SELECT * FROM students WHERE gpa BETWEEN ? AND ?",
        "params": (3.0, 4.0),
        "index_name": "idx_students_gpa",
        "index_columns": "gpa"
    },
    {
        "name": "Query by Last Name",
        "sql": "SELECT * FROM students WHERE last_name = ?",
        "params": ("Smith",),
        "index_name": "idx_students_last_name",
        "index_columns": "last_name"
    },
    {
        "name": "Query by Major and GPA",
        "sql": "SELECT * FROM students WHERE major = ? AND gpa > ?",
        "params": ("Computer Science", 3.5),
        "index_name": "idx_students_major_gpa",
        "index_columns": ["major", "gpa"]
    }
]

# Test each query before and after indexing
for query_info in queries:
    print(f"\n--- {query_info['name']} ---")
    
    # Explain the query before indexing
    print("\nExecution plan BEFORE indexing:")
    plan = explain_query(query_info['sql'], query_info['params'])
    for row in plan:
        print(f"Step {row[0]}: {row[3]}")
    
    # Measure performance before indexing
    time_before = measure_query_performance(query_info['sql'], query_info['params'])
    print(f"Average execution time BEFORE indexing: {time_before*1000:.6f} ms")
    
    # Create the index
    create_index(query_info['index_name'], "students", query_info['index_columns'])
    
    # Explain the query after indexing
    print("\nExecution plan AFTER indexing:")
    plan = explain_query(query_info['sql'], query_info['params'])
    for row in plan:
        print(f"Step {row[0]}: {row[3]}")
    
    # Measure performance after indexing
    time_after = measure_query_performance(query_info['sql'], query_info['params'])
    print(f"Average execution time AFTER indexing: {time_after*1000:.6f} ms")
    
    # Calculate improvement
    if time_before > 0:
        improvement = (time_before - time_after) / time_before * 100
        print(f"Performance improvement: {improvement:.2f}%")

# Show all indexes after optimization
print("\n--- Final Database Indexes ---")
show_indexes("students")

# Demonstrate a complex query with multiple conditions
print("\n--- Complex Query Optimization ---")
complex_query = """
SELECT s.id, s.first_name, s.last_name, s.major, s.gpa
FROM students s
WHERE s.major IN ('Computer Science', 'Mathematics', 'Physics')
AND s.gpa >= ?
ORDER BY s.gpa DESC, s.last_name ASC
"""

# Explain and measure before composite index
print("\nExecution plan BEFORE composite indexing:")
plan = explain_query(complex_query, (3.5,))
for row in plan:
    print(f"Step {row[0]}: {row[3]}")

time_before = measure_query_performance(complex_query, (3.5,))
print(f"Average execution time BEFORE composite indexing: {time_before*1000:.6f} ms")

# Create a composite index for the complex query
create_index("idx_students_major_gpa_lastname", "students", ["major", "gpa", "last_name"])

# Explain and measure after composite index
print("\nExecution plan AFTER composite indexing:")
plan = explain_query(complex_query, (3.5,))
for row in plan:
    print(f"Step {row[0]}: {row[3]}")

time_after = measure_query_performance(complex_query, (3.5,))
print(f"Average execution time AFTER composite indexing: {time_after*1000:.6f} ms")

# Calculate improvement
if time_before > 0:
    improvement = (time_before - time_after) / time_before * 100
    print(f"Performance improvement: {improvement:.2f}%")

print("\nQuery optimization tutorial completed!")