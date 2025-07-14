from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q, Count
from .models import Course, Instructor, Enrollment

# Class-based view equivalent of course_list function
class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'
    
    def get_queryset(self):
        queryset = Course.objects.filter(is_active=True)
        
        # Get query parameters
        query = self.request.GET.get('q', '')
        level = self.request.GET.get('level', '')
        
        # Apply search filter
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | 
                Q(code__icontains=query) | 
                Q(description__icontains=query)
            )
        
        # Apply level filter
        if level and level in dict(Course.LEVEL_CHOICES):
            queryset = queryset.filter(level=level)
        
        # Annotate with enrollment count
        queryset = queryset.annotate(enrolled_students=Count('enrollments'))
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['level'] = self.request.GET.get('level', '')
        context['level_choices'] = Course.LEVEL_CHOICES
        return context

# Class-based view equivalent of course_detail function
class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'
    slug_field = 'code'
    slug_url_kwarg = 'course_code'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        
        # Check if user is enrolled
        is_enrolled = False
        if self.request.user.is_authenticated:
            is_enrolled = Enrollment.objects.filter(
                student=self.request.user, 
                course=course
            ).exists()
        
        # Get prerequisites
        prerequisites = course.prerequisites.all()
        
        # Get related courses
        related_courses = Course.objects.filter(
            Q(instructor=course.instructor) | Q(level=course.level)
        ).exclude(id=course.id)[:3]
        
        context['is_enrolled'] = is_enrolled
        context['prerequisites'] = prerequisites
        context['related_courses'] = related_courses
        
        return context

# Class-based view for My Courses
class MyCourseListView(LoginRequiredMixin, ListView):
    template_name = 'courses/my_courses.html'
    context_object_name = 'enrollments'
    
    def get_queryset(self):
        return Enrollment.objects.filter(student=self.request.user).select_related('course')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        enrollments = self.get_queryset()
        
        # Group by status
        context['active_enrollments'] = enrollments.filter(status='ENR')
        context['completed_enrollments'] = enrollments.filter(status='CMP')
        context['dropped_enrollments'] = enrollments.filter(status='DRP')
        
        return context