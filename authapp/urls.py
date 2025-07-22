from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', auth_views.LogoutView.as_view(template_name='authapp/logout.html'), name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('change-password/', views.change_password_view, name='change_password'),
    path('dashboard/', views.student_dashboard, name='dashboard'),
    path('form-validation-example/', views.form_validation_example, name='form_validation_example'),
]