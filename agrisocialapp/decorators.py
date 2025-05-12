from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def membership_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        if not hasattr(request.user, 'userprofile') or not request.user.userprofile.has_membership:
            messages.warning(request, "This page is for members only.")
            return redirect('profile', pk=request.user.pk)

        return view_func(request, *args, **kwargs)
    return _wrapped_view