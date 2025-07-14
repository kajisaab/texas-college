from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from functools import wraps

def student_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the user is a student,
    redirecting to the login page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and hasattr(u, 'student'),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def instructor_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the user is an instructor,
    redirecting to the login page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and hasattr(u, 'instructor'),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def admin_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the user is an admin,
    redirecting to the login page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.is_staff,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def require_ajax(view_func):
    """
    Decorator for views that checks that the request is an AJAX request.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return view_func(request, *args, **kwargs)
        raise PermissionDenied()
    return _wrapped_view