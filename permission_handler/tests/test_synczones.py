from django.core.management import call_command
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
import requests

import user_variables
from dynatrace.requests.request_handler import generate_tenant_url, no_ssl_verification

from maintenance.models import ZonePerms as maintenance_zone_perms
# Create your tests here.


class SyncZoneTests(TestCase):
  def check_zones_by_content_type(self, content_type_class, codename_list):
    fail_list = []
    for codename in codename_list:
      if not Permission.objects.filter(codename=codename, content_type=ContentType.objects.get_for_model(content_type_class)).exists():
        fail_list.append(f"{content_type_class} | {codename}")

    return fail_list

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

    codename_list = [
        "Dynatrace_LIVE|tenant1|Home",
        "Dynatrace_LIVE|tenant1|Home - Docker",
        "Dynatrace_LIVE|tenant1|easyTravel",
        "Dynatrace_LIVE|tenant1|easyTravel - Test"
    ]

    fail_list = []

    content_type_list = [
        maintenance_zone_perms
    ]

    for content_type_class in content_type_list:
      fail_list = fail_list + \
          self.check_zones_by_content_type(content_type_class, codename_list)

    self.assertEquals(fail_list, [])
