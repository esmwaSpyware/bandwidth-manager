# network/decorators.py
from django.http import HttpResponseForbidden

def role_required(required_roles):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            user_role = UserRole.objects.get(user=request.user).role.name
            if user_role not in required_roles:
                return HttpResponseForbidden()
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
