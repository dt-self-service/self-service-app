from django.shortcuts import render
from .forms import add_allowed_host
from .forms import add_smtp_host
from django.http import HttpResponseRedirect
import fileinput


import tools.setup_settings

from dynatrace_admin.settings import SETTINGS_TEMP_FILE

from tools.setup_settings import generate_allowed_hosts, parse_boolean

# Create your views here.

def initial(request):
  form = add_allowed_host()
  if request.method == 'POST':
    form = add_allowed_host(request.POST)
    # check whether it's valid:
    print(form.is_valid())
    if form.is_valid():
        # process the data in form.cleaned_data as required
        # ...
        # redirect to a new URL:
        data = form.cleaned_data
        for line in fileinput.input(SETTINGS_TEMP_FILE, inplace=True):
          if line.startswith('ALLOWED_HOSTS ='):
            print(generate_allowed_hosts({data['allowed_host']}))
            continue

          if line.startswith('ALLLOWED_HOST_FLAG ='):
            print('ALLLOWED_HOST_FLAG = True')
            continue
          print(line, end='')
        return HttpResponseRedirect('/setup/smtp')
  else:
    form = add_allowed_host()
  return render(request, 'setup/initial.html', {'form': form})


def smtp(request):
  form = add_smtp_host()
  if request.method == 'POST':
    form = add_smtp_host(request.POST)
    # check whether it's valid:
    #print(form.is_valid())
    if form.is_valid():
        # process the data in form.cleaned_data as required
        # ...
        # redirect to a new URL:
        data = form.cleaned_data
        print('string data = ' + str(data['smtp_host']))

        for line in fileinput.input(SETTINGS_TEMP_FILE, inplace=True):
          if line.startswith("EMAIL_HOST ="):
            if data['smtp_host']:
              print("EMAIL_HOST = \"" + str(data['smtp_host']) + "\"")
              continue
          if line.startswith("EMAIL_PORT ="):
            if data['smtp_port']:
              print("EMAIL_PORT = " + str(data['smtp_port']))
              continue
          if line.startswith("EMAIL_HOST_USER ="):
            if data['smtp_host_user']:
              print("EMAIL_HOST_USER = \"" + data['smtp_host_user'] + "\"")
              continue
          if line.startswith("EMAIL_HOST_PASSWORD ="):
            if data['smtp_host_password']:
              print("EMAIL_HOST_PASSWORD = \"" + data['smtp_host_password'] + "\"")
              continue
          if line.startswith("EMAIL_USE_TLS ="):
            if data['smtp_use_tls']:
              print("EMAIL_USE_TLS = " + str(parse_boolean(data['smtp_use_tls'])))
              continue
          if line.startswith("DEFAULT_FROM_EMAIL ="):
            if data['smtp_sender_email']:
              print("DEFAULT_FROM_EMAIL = \"" + str(data['smtp_sender_email']) + "\"")
              continue
          #Set flag
          if line.startswith('SMTP_FLAG ='):
            print('SMTP_FLAG = True')
            continue
          print(line, end='')
        return HttpResponseRedirect('/setup/finish')
    
  return render(request, 'setup/smtp.html', {'form': form})


def finish(request):
  for line in fileinput.input(SETTINGS_TEMP_FILE, inplace=True):
    if line.startswith('SETUP_FLAG ='):
      print('SETUP_FLAG = True')
      continue
    print(line, end='')

  
  return render(request, 'setup/finish.html')