"""Validate User Authication Permissions"""
from django.core.exceptions import PermissionDenied

def is_general_user (request):
  if not request.user.is_authenticated:
    raise PermissionDenied

def is_member_of_group(request, group_name):
  if not request.user.is_authenticated:
    raise PermissionDenied
  else:
    if not request.user.groups.filter(name=group_name).exists():
      raise PermissionDenied