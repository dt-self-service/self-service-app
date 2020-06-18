from django.core.management import call_command
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from django.db import connections
import requests

import user_variables
from dynatrace.requests.request_handler import generate_tenant_url, no_ssl_verification

from maintenance.models import ZonePerms as maintenance_zone_perms
# Create your tests here.


class SyncZoneAdd(TestCase):
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
      },
      "times": {
          "remainingTimes": 1,
          "unlimited": False
      },
      "id": "SyncZones"
  }]

  name_list = [
      "Dynatrace_LIVE|tenant1|Home",
      "Dynatrace_LIVE|tenant1|Home - Docker",
      "Dynatrace_LIVE|tenant1|easyTravel",
      "Dynatrace_LIVE|tenant1|easyTravel - Test"
  ]

  def check_zones_by_content_type(self, content_type_class, name_list):
    fail_list = []
    for name in name_list:
      if not Permission.objects.filter(name=name, content_type=ContentType.objects.get_for_model(content_type_class)).exists():
        fail_list.append(f"{ContentType.objects.get_for_model(content_type_class)} | {name}")

    return fail_list

  def run_sync(self, mock_json, name_list):
    with no_ssl_verification():
      requests.put(self.mock_server_ex, json=mock_json, verify=False)
    call_command('synczones')

    fail_list = []

    content_type_list = [
        maintenance_zone_perms
    ]

    for content_type_class in content_type_list:
      fail_list = fail_list + \
          self.check_zones_by_content_type(content_type_class, name_list)

    return fail_list

  def test_mz_sync(self):
    self.assertEquals(self.run_sync(self.mock_json,self.name_list), [])
    call_command('flush', '--no-input')

class SyncZoneDeleted(TestCase):
  def test_mz_removed(self):
    sync_zone_add = SyncZoneAdd()
    fail_list = sync_zone_add.run_sync(sync_zone_add.mock_json,sync_zone_add.name_list)
    mock_json = sync_zone_add.mock_json.copy()
    name_list = sync_zone_add.name_list.copy()
    
    mock_json[0]["httpResponse"]["body"]["json"]['values'].pop(0) #Removing the "HOME" MZ
    name_list[0] = "REMOVED - Dynatrace_LIVE|tenant1|Home"
    fail_list = fail_list + sync_zone_add.run_sync(mock_json, name_list)

    self.assertEquals(fail_list, [])
    call_command('flush', '--no-input')
