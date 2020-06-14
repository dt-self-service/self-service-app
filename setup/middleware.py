from django.conf import settings
from dynatrace_admin import settings as project_settings
from django.http import (HttpResponseRedirect)

class SetupConfig:
  def __init__(self,get_response):
    self.get_response = get_response

  def __call__(self, request):

    print(request.META['PATH_INFO'])
    #print ('*' in project_settings.ALLOWED_HOSTS)
    # if request.META['PATH_INFO'] != '/setup/initial/' and '*' in project_settings.ALLOWED_HOSTS:
    #  #  print("inside")
    #    return HttpResponseRedirect('/setup/initial/')
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
      if path.startswith('/setup/'):
        return False
      else:
        return True
    else:
      return False