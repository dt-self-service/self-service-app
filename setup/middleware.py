from django.conf import settings
from dynatrace_admin import settings as project_settings
from django.http import (HttpResponseRedirect)

class SetupConfig:
  def __init__(self,get_response):
    self.get_response = get_response

  def __call__(self, request):

    print(request.META['PATH_INFO'])
    if self.is_setup_redirect(request.META['PATH_INFO']):
      print('Setup Required')
      return HttpResponseRedirect("/setup/initial")
    else:
      pass
    
    response = self.get_response(request)
    return response


  def is_setup_redirect(self, path):
    #Root, accounts/* and sso/ allowed without Auth
    if project_settings.SETUP_FLAG == False:
      return not path.startswith('/setup/')
    else:
      return False