# SQLite Tutorial Project

This project provides a comprehensive introduction to SQLite and SQL basics, with a focus on using SQLite with Python. It covers CRUD operations, parameterized queries, context managers, query optimization, and includes a hands-on student database project.

## Project Structure

- `sqlite_basics.py`: Introduction to SQLite and basic CRUD operations
- `parameterized_queries.py`: Demonstrates parameterized queries and context managers
- `query_optimization.py`: Shows how to optimize queries using EXPLAIN and indexes
- `student_database_project.py`: Hands-on project to build a student database and generate reports
- `students.csv`: Sample student data for the project
- `reports/`: Directory where generated reports are saved

## Prerequisites

To run the scripts in this project, you need:

1. Python 3.6 or higher
2. SQLite3 (included in Python's standard library)
3. Additional libraries for the student database project:
   - pandas
   - matplotlib

You can install the required packages using pip:

```bash
pip install pandas matplotlib
```

## Getting Started

### 1. SQLite Basics

Start with the basics of SQLite and CRUD operations:

```bash
python sqlite_basics.py
```

This script demonstrates:
- Creating a database and tables
- Inserting data from a CSV file
- Querying data with various conditions
- Updating and deleting records

### 2. Parameterized Queries and Context Managers

Learn about secure query practices and resource management:

```bash
python parameterized_queries.py
```

This script demonstrates:
- SQL injection vulnerabilities and how to prevent them
- Using parameterized queries for security
- Using context managers for resource cleanup
- Transaction management

### 3. Query Optimization

Understand how to optimize database queries:

```bash
python query_optimization.py
```

This script demonstrates:
- Using EXPLAIN to understand query execution plans
- Creating indexes to improve query performance
- Measuring performance improvements
- Using composite indexes for complex queries

### 4. Student Database Project

Apply all the concepts in a comprehensive project:

```bash
python student_database_project.py
```

This project demonstrates:
- Building a multi-table database (students, courses, enrollments)
- Importing data from CSV
- Generating various reports with complex SQL queries
- Creating visualizations of the data
- Exporting reports to CSV files

## Key Concepts Covered

1. **SQLite Basics**:
   - Database and table creation
   - CRUD operations (Create, Read, Update, Delete)
   - SQL syntax and common commands

2. **Python Integration**:
   - Using the `sqlite3` module
   - Cursor and connection objects
   - Fetching and processing results

3. **Best Practices**:
   - Parameterized queries for security
   - Context managers for resource management
   - Transaction handling
   - Error handling

4. **Performance Optimization**:
   - Using EXPLAIN to analyze queries
   - Creating and using indexes
   - Measuring query performance
   - Optimizing complex queries

5. **Practical Application**:
   - Multi-table database design
   - Relationships between tables (foreign keys)
   - Complex reporting queries
   - Data visualization and export

## Additional Resources

- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Python sqlite3 Module Documentation](https://docs.python.org/3/library/sqlite3.html)
- [SQL Tutorial on W3Schools](https://www.w3schools.com/sql/)
- [SQLite Tutorial on SQLiteTutorial.net](https://www.sqlitetutorial.net/)