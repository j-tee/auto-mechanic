from django.contrib.admin.views.decorators import staff_member_required
from django.urls import resolve


class AdminExcludeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip JWT processing for admin URLs
        if request.path.startswith('/admin/'):
            request._dont_enforce_csrf_checks = False
        response = self.get_response(request)
        return response


class AdminSessionMiddleware:
    """
    Middleware to handle admin routes with session authentication only
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # For admin URLs, ensure we use session authentication only
        if request.path.startswith('/admin/'):
            # Remove any JWT tokens from the request
            if 'HTTP_AUTHORIZATION' in request.META:
                del request.META['HTTP_AUTHORIZATION']

            # Ensure CSRF is properly handled for admin
            request._dont_enforce_csrf_checks = False

        response = self.get_response(request)
        return response
class AdminBypassMiddleware:
    """
    Completely bypass JWT authentication for admin URLs
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # For admin URLs, remove JWT authentication entirely
        if request.path_info.startswith('/admin/'):
            # Clear any Authorization header
            if hasattr(request, 'META') and 'HTTP_AUTHORIZATION' in request.META:
                del request.META['HTTP_AUTHORIZATION']
            
            # Mark this request to skip JWT middleware
            request._skip_jwt = True
        
        response = self.get_response(request)
        return response