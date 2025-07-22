from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import StudentRegistrationForm, StudentProfileForm, ValidationExampleForm
from .models import Student
from .decorators import student_required
from courses.models import Enrollment

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'courses:course_list')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'authapp/login.html')

def register_view(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = StudentRegistrationForm()
    return render(request, 'authapp/register.html', {'form': form})

@login_required
def profile_view(request):
    try:
        student = request.user.student
    except Student.DoesNotExist:
        # If the user doesn't have a student profile, create one
        student = Student.objects.create(
            user=request.user,
            student_id=f"S{request.user.id:06d}"
        )
    
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        form = StudentProfileForm(instance=student)
    
    return render(request, 'authapp/profile.html', {'form': form})

@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'authapp/change_password.html', {'form': form})

@login_required
@student_required
def student_dashboard(request):
    # Get all enrollments for the current student
    enrollments = Enrollment.objects.filter(student=request.user)
    
    context = {
        'enrollments': enrollments,
    }
    return render(request, 'authapp/student_dashboard.html', context)


def form_validation_example(request):
    if request.method == 'POST':
        form = ValidationExampleForm(request.POST)
        if form.is_valid():
            # In a real application, you would save the form data here
            messages.success(request, 'Form submitted successfully!')
            return redirect('form_validation_example')
    else:
        form = ValidationExampleForm()
    
    return render(request, 'authapp/form_validation_example.html', {'form': form})
