from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import render
from django.http import JsonResponse
from django.http import (HttpResponse, HttpResponseRedirect,
                         HttpResponseServerError)
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings

from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.settings import OneLogin_Saml2_Settings
from onelogin.saml2.utils import OneLogin_Saml2_Utils

def init_saml_auth(req):
  auth = OneLogin_Saml2_Auth(req, custom_base_path=settings.SAML_FOLDER)
  return auth


def prepare_django_request(request):
  # If server is behind proxys or balancers use the HTTP_X_FORWARDED fields
  result = {
      'https': 'on' if request.is_secure() else 'off',
      'http_host': request.META['HTTP_HOST'],
      'script_name': request.META['PATH_INFO'],
      'server_port': request.META['SERVER_PORT'],
      'get_data': request.GET.copy(),
      # Uncomment if using ADFS as IdP, https://github.com/onelogin/python-saml/pull/144
      # 'lowercase_urlencoding': True,
      'post_data': request.POST.copy()
  }
  #When Running behind a Proxy, the App needs to be passed this info and adapt
  if 'HTTP_X_FORWARDED_PROTO' in request.META:
    result['https'] = request.META['HTTP_X_FORWARDED_PROTO']
  if 'HTTP_X_FORWARDED_PORT' in request.META:
    result['server_port'] = request.META['HTTP_X_FORWARDED_PORT']
  if 'HTTP_X_FORWARDED_DOMAIN' in request.META:
    result['http_host'] = request.META['HTTP_X_FORWARDED_DOMAIN']
  return result

@csrf_exempt
def index(request):
  req = prepare_django_request(request)
  auth = init_saml_auth(req)
  errors = []
  error_reason = None
  not_auth_warn = False
  success_slo = False
  attributes = False
  paint_logout = False

  print ("Session: " + str(request.session.items()))

  if 'sso' in req['get_data']:
    # If AuthNRequest ID need to be stored in order to later validate it, do instead
    sso_built_url = auth.login()
    request.session['AuthNRequestID'] = auth.get_last_request_id()
    return HttpResponseRedirect(sso_built_url)
  elif 'sso2' in req['get_data']:
    return_to = OneLogin_Saml2_Utils.get_self_url(req)
    return HttpResponseRedirect(auth.login(return_to))
  elif 'slo' in req['get_data']:
    name_id = session_index = name_id_format = name_id_nq = name_id_spnq = None
    if 'samlNameId' in request.session:
      name_id = request.session['samlNameId']
    if 'samlSessionIndex' in request.session:
      session_index = request.session['samlSessionIndex']
    if 'samlNameIdFormat' in request.session:
      name_id_format = request.session['samlNameIdFormat']
    if 'samlNameIdNameQualifier' in request.session:
      name_id_nq = request.session['samlNameIdNameQualifier']
    if 'samlNameIdSPNameQualifier' in request.session:
      name_id_spnq = request.session['samlNameIdSPNameQualifier']

    # If LogoutRequest ID need to be stored in order to later validate it, do instead
    slo_built_url = auth.logout(return_to="/",name_id=name_id, session_index=session_index, nq=name_id_nq, name_id_format=name_id_format, spnq=name_id_spnq)
    request.session['LogoutRequestID'] = auth.get_last_request_id()
    return HttpResponseRedirect(slo_built_url)
  elif 'acs' in req['get_data']:
    request_id = None
    if 'AuthNRequestID' in request.session:
      request_id = request.session['AuthNRequestID']

    auth.process_response(request_id=request_id)
    errors = auth.get_errors()
    not_auth_warn = not auth.is_authenticated()

    if not errors:
      if 'AuthNRequestID' in request.session:
        del request.session['AuthNRequestID']
      request.session['samlUserdata'] = auth.get_attributes()
      request.session['samlNameId'] = auth.get_nameid()
      request.session['samlNameIdFormat'] = auth.get_nameid_format()
      request.session['samlNameIdNameQualifier'] = auth.get_nameid_nq()
      request.session['samlNameIdSPNameQualifier'] = auth.get_nameid_spnq()
      request.session['samlSessionIndex'] = auth.get_session_index()
      if auth.get_settings().is_debug_active():
        print (request)
      if 'RelayState' in req['post_data'] and OneLogin_Saml2_Utils.get_self_url(req) != req['post_data']['RelayState']:
        return HttpResponseRedirect(auth.redirect_to(req['post_data']['RelayState']))
    elif auth.get_settings().is_debug_active():
      error_reason = auth.get_last_error_reason()
      print (error_reason)
  elif 'sls' in req['get_data']:
    request_id = None
    if 'LogoutRequestID' in request.session:
      request_id = request.session['LogoutRequestID']
    dscb = lambda: request.session.flush()
    url = auth.process_slo(request_id=request_id, delete_session_cb=dscb)
    errors = auth.get_errors()
    if len(errors) == 0:
      if url is not None:
        return HttpResponseRedirect(url)
      else:
        success_slo = True
    elif auth.get_settings().is_debug_active():
      error_reason = auth.get_last_error_reason()

  if 'samlUserdata' in request.session:
    paint_logout = True
    if len(request.session['samlUserdata']) > 0:
      attributes = request.session['samlUserdata'].items()
  return HttpResponseRedirect("/")

def attrs(request):
  paint_logout = False
  attributes = False

  if 'samlUserdata' in request.session:
    paint_logout = True
    if len(request.session['samlUserdata']) > 0:
      attributes = request.session['samlUserdata'].items()
  return render(request, 'attrs.html',
                {'paint_logout': paint_logout,
                 'attributes': attributes})


def metadata(request):
  saml_settings = OneLogin_Saml2_Settings(settings=None, custom_base_path=settings.SAML_FOLDER, sp_validation_only=True)
  metadata = saml_settings.get_sp_metadata()
  errors = saml_settings.validate_metadata(metadata)

  if len(errors) == 0:
    resp = HttpResponse(content=metadata, content_type='text/xml')
  else:
    resp = HttpResponseServerError(content=', '.join(errors))
  return resp