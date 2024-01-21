from django.core.exceptions import PermissionDenied
from .models import Korisnici

def admin_required(function):
    def wrap(request, *args, **kwargs):
        user = Korisnici.objects.get(pk=request.user.pk)
        if user.role_id == 1 and user.is_authenticated and user.is_active:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap

def student_required(function):
    def wrap(request, *args, **kwargs):
        user = Korisnici.objects.get(pk=request.user.pk)
        if user.role_id == 3 and user.is_authenticated and user.is_active:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap

def profesor_required(function):
    def wrap(request, *args, **kwargs):
        user = Korisnici.objects.get(pk=request.user.pk)
        if user.role_id == 2 and user.is_authenticated and user.is_active:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap

def admin_student_required(function):
    def wrap(request, *args, **kwargs):
        user = Korisnici.objects.get(pk=request.user.pk)
        if (user.role_id == 1 or user.role_id == 3) and user.is_authenticated and user.is_active:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap