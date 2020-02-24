from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib import messages
from functools import wraps
from urllib.parse import urlparse
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.shortcuts import resolve_url


default_message="Access Denied!"

def user_passes_test(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME ,message=default_message):

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)
            else:
                messages.warning(request, message)

            path = request.build_absolute_uri()
            resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
            # If the login url is the same scheme and net location then just
            # use the path as the "next" url.
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if ((not login_scheme or login_scheme == current_scheme) and
                    (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(
                path, resolved_login_url, redirect_field_name)
        return _wrapped_view
    return decorator

def instructor_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='/', message="Access denied. Please login with instructor account!"):

    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.is_active and u.is_instructor and (not u.is_student),
        login_url=login_url,
        redirect_field_name=redirect_field_name,
        message=message
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def student_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='/', message="Access denied. Please login with student account!"):

    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.is_active and u.is_student,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
        message=message
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def ta_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='/', message="Access denied. Are you a TA for any course?"):

    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.is_active and u.is_student and u.is_instructor,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
        message=message
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def ta_or_instructor_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='/', message="Access denied. Are you an instructor or TA for any course?"):

    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.is_active and u.is_instructor,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
        message=message
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def student_or_instructor_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='/', message="Access denied. Please login with cmu account!"):

    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.is_active and (u.is_student or u.is_instructor),
        login_url=login_url,
        redirect_field_name=redirect_field_name,
        message=message
    )
    if function:
        return actual_decorator(function)
    return actual_decorator