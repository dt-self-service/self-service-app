"""Generate secret key for first run"""
import fileinput
import argparse
from django.core.management.utils import get_random_secret_key

def generate_allowed_hosts(allowed_hosts):
  allowed_string = "ALLOWED_HOSTS = ["
  for host in allowed_hosts:
    allowed_string = allowed_string + "'" +str(host) + "',"
  allowed_string = allowed_string[:-1] + "]"
  return allowed_string

def parse_boolean (debug_flag):
  if isinstance(debug_flag, (bool)):
    return debug_flag
  if isinstance(debug_flag, (str)):
    if debug_flag.upper() == "FALSE":
      return False
    if debug_flag.upper() == "TRUE":
      return True
  return False #TODO Raise Exception for Invalid Input

def setup_settings_file(args):
  """Replace Secret Key in settings.py"""
  for line in fileinput.input(args.settings_file, inplace=True):
    if line.startswith("SECRET_KEY ="):
      print ("SECRET_KEY = '",get_random_secret_key(),"'",sep="")
      continue
    if line.startswith("ALLOWED_HOSTS ="):
      print (generate_allowed_hosts(args.allowed_hosts))
      continue
    if line.startswith("DEBUG ="):
      print ("DEBUG = " + str(parse_boolean(args.debug)))
      continue
    if line.startswith("EMAIL_HOST ="):
      if args.smtp_host:
        print("EMAIL_HOST = \"" + str(args.smtp_host) + "\"")
        continue
    if line.startswith("EMAIL_PORT ="):
      if args.smtp_port:
        print("EMAIL_PORT = " + str(args.smtp_port))
        continue
    if line.startswith("EMAIL_HOST_USER ="):
      if args.smtp_host_user:
        print("EMAIL_HOST_USER = \"" + str(args.smtp_host_user) + "\"")
        continue
    if line.startswith("EMAIL_HOST_PASSWORD ="):
      if args.smtp_host_password:
        print("EMAIL_HOST_PASSWORD = \"" + str(args.smtp_host_password) + "\"")
        continue
    if line.startswith("EMAIL_USE_TLS ="):
      if args.smtp_use_tls:
        print("EMAIL_USE_TLS = " + str(parse_boolean(args.smtp_use_tls)))
        continue
    if line.startswith("DEFAULT_FROM_EMAIL ="):
      if args.smtp_sender_email:
        print("DEFAULT_FROM_EMAIL = \"" + str(args.smtp_sender_email) + "\"")
        continue
    
    print(line, end="")

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--settings-file', required=True)
  parser.add_argument('--debug', '-d', default=False) #TODO Function for Debug
  parser.add_argument('--allowed-hosts',required=True, nargs='+') #TODO Function
  parser.add_argument('--smtp-host')
  parser.add_argument('--smtp-port')
  parser.add_argument('--smtp-host-user')
  parser.add_argument('--smtp-host-password')
  parser.add_argument('--smtp-use-tls', default=True)
  parser.add_argument('--smtp-sender-email')

  args = parser.parse_args()
  print (args)
  setup_settings_file(args)
