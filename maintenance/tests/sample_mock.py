from django.test import TestCase
from django.http import QueryDict

from maintenance import views

from django.contrib.auth.models import User
from django.test import Client
import user_variables as uv


import requests, json

from dynatrace.requests.request_handler import no_ssl_verification



class ViewsTests(TestCase):
    def test_mock_sample2(self):
        # Making a PUT request 
        # url:
        # https://lhh08344.live.dynatrace.com/api/config/v1/maintenanceWindows
        # params
        # {'Api-Token': 'EO0Yq0dsQPyhrgHz1VxpH'}
        # json:
        # {'name': 'MockServer2', 'description': 'MockServer', 'suppression': 'DETECT_PROBLEMS_AND_ALERT', 'schedule': {'recurrenceType': 'ONCE', 'start': '2019-01-15 23:00', 'end': '2019-01-15 23:04', 'zoneId': 'America/Toronto'}, 'type': 'PLANNED', 'scope': {'entities': [], 'matches': [{'type': 'OS', 'managementZoneId': 'null', 'tags': [{'context': 'CONTEXTLESS', 'key': 'Windows'}]}]}}
        # [13/May/2020 20:17:09] "POST /maintenance/submit_create HTTP/1.1" 200 3

        # sample request:
        # {'id': '90916273-5320-410c-b7a0-5548711b52f1', 'name': 'MockServer2', 'description': 'MockServer'}

        # To find some more details, you want to print the response.POST from requests on the views.py page.
        # To find query data for mocks, you want to add the followinglines to the request handler from the framework:
        # print("url: \n" + generate_tenant_url(cluster, tenant) + "/api/config/v1/" + endpoint)
        # print("params")
        # print(params)
        # print("json:")
        # print(json)

       

        mock_server_ex = 'https://localhost:1080/mockserver/expectation'
        data = [{
            "httpRequest" : {
                "method" : "POST",
                "path" : "/api/config/v1/maintenanceWindows",
                "queryStringParameters" : {
                    "Api-Token" : [ "EO0Yq0dsQPyhrgHz1VxpH" ]
                },
                "body": {
                    "type": "JSON",
                    "json": {'name': 'MockServer2', 'description': 'MockServer', 'suppression': 'DETECT_PROBLEMS_AND_ALERT', 'schedule': {'recurrenceType': 'ONCE', 'start': '2019-01-15 23:00', 'end': '2019-01-15 23:04', 'zoneId': 'America/Toronto'}, 'type': 'PLANNED', 'scope': {'entities': [], 'matches': [{'type': 'OS', 'managementZoneId': 'null', 'tags': [{'context': 'CONTEXTLESS', 'key': 'Windows'}]}]}},
                "matchType": "ONLY_MATCHIG_FIELDS"
                }
            
            },
            "httpResponse" : {
                "body" : {
                    "type": "JSON",
                    "json": {'id': '90916273-5320-410c-b7a0-5548711b52f1', 'name': 'MockServer2', 'description': 'MockServer'}
                }
            }
        }]

        headers = {"Content-Type": "application/json"}

        with no_ssl_verification():
            response = requests.put(mock_server_ex, data=json.dumps(data), verify=False, headers=headers)
            print(response)

        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()

        c = Client()
        c.login(username='testuser', password='12345')
        response = c.post('/maintenance/submit_create', {'csrfmiddlewaretoken': ['qtotVIAInv38Qwrc2uwFAL5M4An06P8j1aBjscPwMpSnTUbBmYVMFYihe1lqzjC8'], 'cluster_name': ['Dynatrace_LIVE'], 'tenant_name': ['tenant1'], 'window_name': ['MockServer2'], 'window_planned': ['True'], 'window_description': ['MockServer'], 'window_recurrence': ['ONCE'], 'window_day_of_week': [''], 'window_day_of_month': ['1'], 'window_supression': ['DETECT_PROBLEMS_AND_ALERT'], 'window_start_time': [''], 'window_duration': [''], 'window_maintenance_start': ['2019-01-15 23:00'], 'window_maintenance_end': ['2019-01-15 23:04'], 'form-TOTAL_FORMS': ['1'], 'form-INITIAL_FORMS': ['0'], 'form-MIN_NUM_FORMS': ['0'], 'form-MAX_NUM_FORMS': ['10'], 'form-0-entity_type': ['OS'], 'form-0-tags_or_entities': ['TAGS'], 'form-0-filter_value': ['Windows'], 'form-__prefix__-entity_type': [''], 'form-__prefix__-tags_or_entities': [''], 'form-__prefix__-filter_value': ['']})

        self.assertEquals(response.status_code, 200)


