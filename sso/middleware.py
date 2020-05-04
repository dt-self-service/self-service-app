from django.conf import settings
from django.http import (HttpResponseRedirect)

from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.settings import OneLogin_Saml2_Settings
from onelogin.saml2.utils import OneLogin_Saml2_Utils

class SamlAuth:
  def __init__(self,get_response):
    self.get_response = get_response

  def __call__(self, request):
    if 'samlNameId' in request.session:
      print ("SAML NameID: " + str(request.session['samlNameId']))
    elif request.user.is_authenticated:
      print ("Local User")
    elif self.is_login_required(request.META['PATH_INFO']):
      print ("Login required")
      return HttpResponseRedirect("/accounts/login/")
    else:
      print ("Not Logged In")
      print ("Request URL: " + str(request.META['PATH_INFO']))
      # print ("SAML UserData: " + str(request.session['samlUserdata']))
      # print ("SAML SessionIndex: " + str(request.session['samlSessionIndex']))
      # print ("Session: " + str(request.session.items()))
      
    
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