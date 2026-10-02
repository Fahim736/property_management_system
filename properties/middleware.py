from django.shortcuts import redirect
from django.contrib import messages

class RoleBasedAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            path = request.path
            # Prevent Tenants from accessing Owner Dashboard
            if path.startswith('/owner-dashboard/') and not request.user.is_owner():
                messages.error(request, "Access restricted to Property Owners.")
                return redirect('tenant_dashboard')
            # Prevent Owners from accessing Tenant Dashboard
            elif path.startswith('/tenant-dashboard/') and not request.user.is_tenant():
                messages.error(request, "Access restricted to Tenants.")
                return redirect('owner_dashboard')

        return self.get_response(request)