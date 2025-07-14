from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Count
from .models import Course, Instructor, Enrollment
from .serializers import CourseSerializer, InstructorSerializer, EnrollmentSerializer

class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for courses
    """
    queryset = Course.objects.filter(is_active=True)
    serializer_class = CourseSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'code', 'description']
    
    def get_queryset(self):
        queryset = Course.objects.filter(is_active=True)
        
        # Filter by level if provided
        level = self.request.query_params.get('level', None)
        if level and level in dict(Course.LEVEL_CHOICES):
            queryset = queryset.filter(level=level)
        
        # Search if query parameter provided
        query = self.request.query_params.get('q', None)
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | 
                Q(code__icontains=query) | 
                Q(description__icontains=query)
            )
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """
        Return a list of featured courses (most enrolled)
        """
        courses = Course.objects.filter(is_active=True)\
            .annotate(enrollment_count=Count('enrollments'))\
            .order_by('-enrollment_count')[:5]
        
        serializer = self.get_serializer(courses, many=True)
        return Response(serializer.data)

class InstructorViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for instructors
    """
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer

class EnrollmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for enrollments
    """
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Users can only see their own enrollments
        return Enrollment.objects.filter(student=self.request.user)
    
    def perform_create(self, serializer):
        # Set the student to the current user
        serializer.save(student=self.request.user)