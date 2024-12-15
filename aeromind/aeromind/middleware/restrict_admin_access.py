# aeromind/middleware/restrict_admin_access.py

from django.http import HttpResponseForbidden

class AdminAccessMiddleware:
    """
    Middleware to restrict access to the Django admin panel
    only for superusers. Admin users (with is_staff = True)
    cannot access the Django admin panel.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # If the user is trying to access the admin panel and is not a superuser, deny access
        if request.path.startswith('/admin/') and not request.user.is_superuser:
            return HttpResponseForbidden("You are not authorized to access the admin panel.")
        
        # Continue processing the request if the user is allowed
        response = self.get_response(request)
        return response
