"""Validate User Authication Permissions"""
from django.core.exceptions import PermissionDenied

def is_general_user (request):
  if not request.user.is_authenticated:
    raise PermissionDenied