from django.conf import settings
from django.http import (HttpResponseRedirect, HttpResponseForbidden)

class SamlAuth:
  def __init__(self,get_response):
    self.get_response = get_response

  def __call__(self, request):
    # Group information can be retreived from request.session['samlUserdata']['member']
    if 'samlNameId' in request.session:
      print (request.session['samlUserdata']['member'])
      if settings.SSO_ADMIN_GROUP in request.session['samlUserdata']['member'] or \
          settings.SSO_USER_GROUP in request.session['samlUserdata']['member']:
        pass
      else:
        if self.is_login_required(request.META['PATH_INFO']):
          return HttpResponseForbidden()
        else:
          pass
      # pass
    elif request.user.is_authenticated:
      pass
    elif self.is_login_required(request.META['PATH_INFO']):
      print ("Login required")
      return HttpResponseRedirect("/accounts/login/")
    else:
      pass
      
    
    response = self.get_response(request)
    return response
  def is_login_required(self, path):
    #Root, accounts/* and sso/ allowed without Auth
    if path == "/" \
        or path == "/sso/" \
        or path.startswith("/accounts/") \
        or path.startswith("/admin"):
      return False
    else:
      return True