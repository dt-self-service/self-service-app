from django import forms
from django.forms import formset_factory



class add_allowed_host(forms.Form):
  allowed_host = forms.CharField(
  label='Allowed Host Domain',
  widget = forms.TextInput(
    attrs = {'class': 'form-control'}
      )
  )

class add_smtp_host(forms.Form):
  smtp_host = forms.CharField(
  label = 'SMTP Host URL',
  required = True,
  widget = forms.URLInput(
    attrs = {'class': 'form-control'}
      )
  )

  smtp_port = forms.IntegerField(
  label = 'SMTP Port',
  required=False,
  widget = forms.NumberInput(
    attrs = {'class': 'form-control'}
      )
  )

  smtp_host_user = forms.CharField(
    label = 'SMTP User',
    required = False,
    widget = forms.TextInput(
      attrs = {'class': 'form-control'}
    )
  )

  smtp_host_password = forms.CharField(
    label = 'SMTP Password',
    required = False,
    widget = forms.PasswordInput(
      attrs = {'class': 'form-control'}
    )
  )

  smtp_use_tls = forms.BooleanField(
      label = 'Use TLS?',
      initial=False,
      required = False,
      widget = forms.CheckboxInput(
        attrs = {'class': 'form-control'}
      )
    )

  smtp_sender_email = forms.CharField(
      label = 'SMTP email, TestSite Team <noreply@example.com>',
      required = False,
      widget = forms.TextInput(
        attrs = {'class': 'form-control'}
      )
    )
