from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
import re
from .models import Student

class StudentRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    student_id = forms.CharField(max_length=20, required=True)
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=Student.GENDER_CHOICES, required=False)
    address = forms.CharField(max_length=255, required=False)
    phone_number = forms.CharField(max_length=15, required=False)
    major = forms.CharField(max_length=100, required=False)
    profile_picture = forms.ImageField(required=False)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            student = Student.objects.create(
                user=user,
                student_id=self.cleaned_data['student_id'],
                date_of_birth=self.cleaned_data.get('date_of_birth'),
                gender=self.cleaned_data.get('gender'),
                address=self.cleaned_data.get('address'),
                phone_number=self.cleaned_data.get('phone_number'),
                major=self.cleaned_data.get('major'),
                profile_picture=self.cleaned_data.get('profile_picture')
            )
        
        return user

class StudentProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = Student
        fields = ['student_id', 'date_of_birth', 'gender', 'address', 'phone_number', 'major', 'profile_picture']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
    
    def save(self, commit=True):
        student = super().save(commit=False)
        if commit:
            # Update User model fields
            student.user.first_name = self.cleaned_data['first_name']
            student.user.last_name = self.cleaned_data['last_name']
            student.user.email = self.cleaned_data['email']
            student.user.save()
            student.save()
        return student


class ValidationExampleForm(forms.Form):
    username = forms.CharField(
        min_length=3,
        max_length=20,
        required=True,
        validators=[
            # Custom validator for username format
            lambda value: ValidationError("Username can only contain letters, numbers, and underscores.") 
                if not re.match(r'^[A-Za-z0-9_]+$', value) else None,
        ],
        error_messages={
            'required': 'Username is required.',
            'min_length': 'Username must be at least 3 characters long.',
            'max_length': 'Username cannot be more than 20 characters long.',
        }
    )
    
    email = forms.EmailField(
        required=True,
        error_messages={
            'required': 'Email address is required.',
            'invalid': 'Please enter a valid email address.',
        }
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput,
        min_length=8,
        required=True,
        error_messages={
            'required': 'Password is required.',
            'min_length': 'Password must be at least 8 characters long.',
        }
    )
    
    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        error_messages={
            'required': 'Please confirm your password.',
        }
    )
    
    birth_year = forms.IntegerField(
        required=False,
        min_value=1900,
        max_value=timezone.now().year,
        error_messages={
            'min_value': 'Birth year cannot be earlier than 1900.',
            'max_value': f'Birth year cannot be later than {timezone.now().year}.',
            'invalid': 'Please enter a valid year.',
        }
    )
    
    website = forms.URLField(
        required=False,
        error_messages={
            'invalid': 'Please enter a valid URL (e.g., https://example.com).',
        }
    )
    
    terms = forms.BooleanField(
        required=True,
        error_messages={
            'required': 'You must agree to the terms and conditions.',
        }
    )
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        
        # Check for password strength
        if password:
            # At least one uppercase letter
            if not re.search(r'[A-Z]', password):
                raise ValidationError("Password must contain at least one uppercase letter.")
            
            # At least one lowercase letter
            if not re.search(r'[a-z]', password):
                raise ValidationError("Password must contain at least one lowercase letter.")
            
            # At least one digit
            if not re.search(r'[0-9]', password):
                raise ValidationError("Password must contain at least one number.")
            
            # At least one special character
            if not re.search(r'[^A-Za-z0-9]', password):
                raise ValidationError("Password must contain at least one special character.")
        
        return password
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        # Check if passwords match
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        
        # Example of form-level validation that depends on multiple fields
        email = cleaned_data.get('email')
        username = cleaned_data.get('username')
        
        if email and username and email.split('@')[0].lower() == username.lower():
            self.add_error(None, "Username should not be the same as your email prefix for security reasons.")
        
        return cleaned_data