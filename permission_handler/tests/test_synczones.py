from django.core.management import call_command
from django.contrib.auth.models import Permission
from django.test import TestCase
import requests

import user_variables
from dynatrace.requests.request_handler import generate_tenant_url, no_ssl_verification

# Create your tests here.


class SyncZoneTests(TestCase):
  def test_mz_sync(self):
    mock_server_ex = generate_tenant_url(
        user_variables.FULL_SET['Dynatrace_LIVE'], 'tenant1') + '/mockserver/expectation'
    mock_json = [{
        "httpRequest": {
            "method": "GET",
            "path": "/api/config/v1/managementZones",
            "queryStringParameters": {
                    "Api-Token": ["sample_api_token"]
            },
        },
        "httpResponse": {
            "body": {
                "type": "JSON",
                "json": {'values': [{'id': '-2953693654005874660', 'name': 'Home'}, {'id': '-6695637066915199673', 'name': 'Home - Docker'}, {'id': '-471941985681809325', 'name': 'easyTravel'}, {'id': '3161788351280113535', 'name': 'easyTravel - Test'}]}
            }
        }
    }]

    with no_ssl_verification():
      requests.put(mock_server_ex, json=mock_json)
    call_command('synczones')
    check_all_zones = Permission.objects.filter(codename="Dynatrace_LIVE|tenant1|Home").exists() \
        and Permission.objects.filter(codename="Dynatrace_LIVE|tenant1|Home - Docker").exists() \
        and Permission.objects.filter(codename="Dynatrace_LIVE|tenant1|easyTravel").exists() \
        and Permission.objects.filter(codename="Dynatrace_LIVE|tenant1|easyTravel - Test").exists()
    self.assertEquals(check_all_zones, True)
