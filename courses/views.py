from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from .models import Course, Instructor, Enrollment

def course_list(request):
    """Display a list of all active courses"""
    query = request.GET.get('q', '')
    level = request.GET.get('level', '')
    
    courses = Course.objects.filter(is_active=True)
    
    # Apply search filter
    if query:
        courses = courses.filter(
            Q(title__icontains=query) | 
            Q(code__icontains=query) | 
            Q(description__icontains=query)
        )
    
    # Apply level filter
    if level and level in dict(Course.LEVEL_CHOICES):
        courses = courses.filter(level=level)
    
    # Annotate with enrollment count
    courses = courses.annotate(enrolled_students=Count('enrollments'))
    
    context = {
        'courses': courses,
        'query': query,
        'level': level,
        'level_choices': Course.LEVEL_CHOICES,
    }
    
    return render(request, 'courses/course_list.html', context)

def course_detail(request, course_code):
    """Display details for a specific course"""
    course = get_object_or_404(Course, code=course_code)
    
    # Check if user is enrolled
    is_enrolled = False
    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()
    
    # Get prerequisites
    prerequisites = course.prerequisites.all()
    
    # Get related courses (same instructor or level)
    related_courses = Course.objects.filter(
        Q(instructor=course.instructor) | Q(level=course.level)
    ).exclude(id=course.id)[:3]
    
    context = {
        'course': course,
        'is_enrolled': is_enrolled,
        'prerequisites': prerequisites,
        'related_courses': related_courses,
    }
    
    return render(request, 'courses/course_detail.html', context)

@login_required
def enroll_course(request, course_code):
    """Enroll the current user in a course"""
    course = get_object_or_404(Course, code=course_code)
    
    # Check if already enrolled
    if Enrollment.objects.filter(student=request.user, course=course).exists():
        messages.warning(request, f'You are already enrolled in {course.title}')
        return redirect('courses:course_detail', course_code=course.code)
    
    # Check if course is full
    current_enrollment = Enrollment.objects.filter(course=course, status='ENR').count()
    if current_enrollment >= course.max_students:
        messages.error(request, f'Sorry, {course.title} is already full')
        return redirect('courses:course_detail', course_code=course.code)
    
    # Check prerequisites
    missing_prerequisites = []
    for prereq in course.prerequisites.all():
        if not Enrollment.objects.filter(student=request.user, course=prereq, status='CMP').exists():
            missing_prerequisites.append(prereq)
    
    if missing_prerequisites:
        prereq_list = ', '.join([p.code for p in missing_prerequisites])
        messages.error(request, f'You need to complete these prerequisites first: {prereq_list}')
        return redirect('courses:course_detail', course_code=course.code)
    
    # Create enrollment
    Enrollment.objects.create(student=request.user, course=course, status='ENR')
    messages.success(request, f'You have successfully enrolled in {course.title}')
    
    return redirect('courses:my_courses')

def instructor_detail(request, instructor_id):
    """Display details for a specific instructor"""
    instructor = get_object_or_404(Instructor, id=instructor_id)
    courses = Course.objects.filter(instructor=instructor, is_active=True)
    
    context = {
        'instructor': instructor,
        'courses': courses,
    }
    
    return render(request, 'courses/instructor_detail.html', context)

@login_required
def my_courses(request):
    """Display courses the current user is enrolled in"""
    enrollments = Enrollment.objects.filter(student=request.user).select_related('course')
    
    # Group by status
    active_enrollments = enrollments.filter(status='ENR')
    completed_enrollments = enrollments.filter(status='CMP')
    dropped_enrollments = enrollments.filter(status='DRP')
    
    context = {
        'active_enrollments': active_enrollments,
        'completed_enrollments': completed_enrollments,
        'dropped_enrollments': dropped_enrollments,
    }
    
    return render(request, 'courses/my_courses.html', context)

def course_list_ajax(request):
    """Display a page that loads course data dynamically using Fetch API"""
    return render(request, 'courses/course_list_ajax.html')

def course_list_jquery(request):
    """Display a page that loads course data dynamically using jQuery AJAX"""
    return render(request, 'courses/course_list_jquery.html')
