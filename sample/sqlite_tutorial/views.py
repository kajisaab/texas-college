from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import subprocess
import os
import sys
from pathlib import Path
import json

# Get the current directory
BASE_DIR = Path(__file__).resolve().parent

# Create your views here.
def index(request):
    """Main index page for the SQLite tutorial"""
    context = {
        'title': 'SQLite Tutorial',
        'sections': [
            {
                'name': 'SQLite Basics',
                'url': 'basics/',
                'description': 'Introduction to SQLite and basic CRUD operations'
            },
            {
                'name': 'Parameterized Queries',
                'url': 'parameterized/',
                'description': 'Learn about secure query practices and resource management'
            },
            {
                'name': 'Query Optimization',
                'url': 'optimization/',
                'description': 'Understand how to optimize database queries'
            },
            {
                'name': 'Student Database Project',
                'url': 'project/',
                'description': 'Hands-on project to build a student database and generate reports'
            }
        ]
    }
    return render(request, 'sqlite_tutorial/index.html', context)

def basics(request):
    """View for SQLite basics tutorial"""
    # Read the content of the script file
    script_path = BASE_DIR / 'sqlite_basics.py'
    with open(script_path, 'r') as file:
        script_content = file.read()
    
    context = {
        'title': 'SQLite Basics',
        'script_content': script_content,
        'run_url': 'run_basics'
    }
    return render(request, 'sqlite_tutorial/tutorial_page.html', context)

def parameterized(request):
    """View for parameterized queries tutorial"""
    # Read the content of the script file
    script_path = BASE_DIR / 'parameterized_queries.py'
    with open(script_path, 'r') as file:
        script_content = file.read()
    
    context = {
        'title': 'Parameterized Queries and Context Managers',
        'script_content': script_content,
        'run_url': 'run_parameterized'
    }
    return render(request, 'sqlite_tutorial/tutorial_page.html', context)

def optimization(request):
    """View for query optimization tutorial"""
    # Read the content of the script file
    script_path = BASE_DIR / 'query_optimization.py'
    with open(script_path, 'r') as file:
        script_content = file.read()
    
    context = {
        'title': 'Query Optimization',
        'script_content': script_content,
        'run_url': 'run_optimization'
    }
    return render(request, 'sqlite_tutorial/tutorial_page.html', context)

def project(request):
    """View for student database project"""
    # Read the content of the script file
    script_path = BASE_DIR / 'student_database_project.py'
    with open(script_path, 'r') as file:
        script_content = file.read()
    
    context = {
        'title': 'Student Database Project',
        'script_content': script_content,
        'run_url': 'run_project'
    }
    return render(request, 'sqlite_tutorial/tutorial_page.html', context)

# Run script functions
def run_script(script_name):
    """Helper function to run a Python script and capture its output"""
    script_path = BASE_DIR / script_name
    
    try:
        # Run the script and capture output
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            cwd=str(BASE_DIR)
        )
        
        # Return stdout and stderr
        return {
            'success': result.returncode == 0,
            'output': result.stdout,
            'error': result.stderr
        }
    except Exception as e:
        return {
            'success': False,
            'output': '',
            'error': str(e)
        }

def run_basics(request):
    """Run the SQLite basics script"""
    result = run_script('sqlite_basics.py')
    return JsonResponse(result)

def run_parameterized(request):
    """Run the parameterized queries script"""
    result = run_script('parameterized_queries.py')
    return JsonResponse(result)

def run_optimization(request):
    """Run the query optimization script"""
    result = run_script('query_optimization.py')
    return JsonResponse(result)

def run_project(request):
    """Run the student database project script"""
    result = run_script('student_database_project.py')
    return JsonResponse(result)
