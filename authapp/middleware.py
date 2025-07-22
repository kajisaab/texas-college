from django.utils import timezone
from django.contrib.auth.models import User

class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before the view is called
        response = self.get_response(request)
        # Code to be executed for each request after the view is called
        
        # Update last activity timestamp for authenticated users
        if request.user.is_authenticated:
            # Update User's last_login if it's been more than 1 hour
            if not request.user.last_login or (timezone.now() - request.user.last_login).total_seconds() > 3600:
                User.objects.filter(pk=request.user.pk).update(last_login=timezone.now())
            
            # If the user has a student profile, update its last activity
            try:
                if hasattr(request.user, 'student'):
                    request.user.student.last_activity = timezone.now()
                    request.user.student.save(update_fields=['last_activity'])
            except Exception as e:
                # If there's an error, just continue without updating
                # In a production environment, you might want to log this error
                pass
                
        return response