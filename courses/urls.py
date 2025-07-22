from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from . import api

app_name = 'courses'

# DRF Router for API endpoints
router = DefaultRouter()
router.register(r'api/courses', api.CourseViewSet)
router.register(r'api/instructors', api.InstructorViewSet)
router.register(r'api/enrollments', api.EnrollmentViewSet, basename='enrollment')

urlpatterns = [
    # Regular views
    path('', views.course_list, name='course_list'),
    path('ajax/', views.course_list_ajax, name='course_list_ajax'),
    path('jquery/', views.course_list_jquery, name='course_list_jquery'),
    path('my-courses/', views.my_courses, name='my_courses'),
    path('instructor/<int:instructor_id>/', views.instructor_detail, name='instructor_detail'),
    path('<str:course_code>/enroll/', views.enroll_course, name='enroll_course'),
    path('<str:course_code>/', views.course_detail, name='course_detail'),
    
    # API endpoints
    path('', include(router.urls)),
]