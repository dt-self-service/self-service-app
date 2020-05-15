from django.test import TestCase
from django.http import QueryDict

from maintenance import views

from django.contrib.auth.models import User
from django.test import Client
import user_variables as uv


import requests, json

from dynatrace.requests.request_handler import no_ssl_verification


class ViewsTests(TestCase):
    def test_submit_create(self):
        mock_server_ex = 'https://' + FULL_SET['Dynatrace_LIVE']['url'] + ':/mockserver/expectation'
        data = [{
            "httpRequest" : {
                "method" : "POST",
                "path" : "/api/config/v1/maintenanceWindows",
                "queryStringParameters" : {
                    "Api-Token" : [ "sample_api_token" ]
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
           

        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()

        c = Client()
        c.login(username='testuser', password='12345')
        response = c.post('/maintenance/submit_create', {'csrfmiddlewaretoken': ['qtotVIAInv38Qwrc2uwFAL5M4An06P8j1aBjscPwMpSnTUbBmYVMFYihe1lqzjC8'], 'cluster_name': ['Dynatrace_LIVE'], 'tenant_name': ['tenant1'], 'window_name': ['MockServer2'], 'window_planned': ['True'], 'window_description': ['MockServer'], 'window_recurrence': ['ONCE'], 'window_day_of_week': [''], 'window_day_of_month': ['1'], 'window_supression': ['DETECT_PROBLEMS_AND_ALERT'], 'window_start_time': [''], 'window_duration': [''], 'window_maintenance_start': ['2019-01-15 23:00'], 'window_maintenance_end': ['2019-01-15 23:04'], 'form-TOTAL_FORMS': ['1'], 'form-INITIAL_FORMS': ['0'], 'form-MIN_NUM_FORMS': ['0'], 'form-MAX_NUM_FORMS': ['10'], 'form-0-entity_type': ['OS'], 'form-0-tags_or_entities': ['TAGS'], 'form-0-filter_value': ['Windows'], 'form-__prefix__-entity_type': [''], 'form-__prefix__-tags_or_entities': [''], 'form-__prefix__-filter_value': ['']})

        self.assertEquals(response.status_code, 200)

    def test_submit_update(self):
        mock_server_ex = 'https://' + FULL_SET['Dynatrace_LIVE']['url'] + '/mockserver/expectation'
        data = [{
            "httpRequest" : {
                "method" : "PUT",
                "path" : "/api/config/v1/maintenanceWindows/90916273-5320-410c-b7a0-5548711b52f1",
                "queryStringParameters" : {
                    "Api-Token" : [ "sample_api_token" ]
                },
                "body": {
                    "type": "JSON",
                    "json": {'name': 'Updated Window', 'description': 'Updated', 'suppression': 'DETECT_PROBLEMS_AND_ALERT', 'schedule': {'recurrenceType': 'ONCE', 'start': '2019-01-15 23:00', 'end': '2019-01-15 23:05', 'zoneId': 'America/Toronto'}, 'type': 'PLANNED', 'scope': {'entities': [], 'matches': [{'type': 'OS', 'managementZoneId': 'null', 'tags': [{'context': 'CONTEXTLESS', 'key': 'Windows'}]}]}},
                "matchType": "ONLY_MATCHIG_FIELDS"
                }
            
            },
            "httpResponse" : {
                "statusCode": 204
            }
        }]

        headers = {"Content-Type": "application/json"}
        with no_ssl_verification():
            response = requests.put(mock_server_ex, data=json.dumps(data), verify=False, headers=headers)
           

        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()

        c = Client()
        c.login(username='testuser', password='12345')

        response = c.post('/maintenance/submit_update', {'csrfmiddlewaretoken': ['D33rQHPAKN1qhk62yI1JBpA5O6rPWfhJeKghnb4o9HQFkIQrScqQGCNAYxpfpJLy'], 'cluster_name': ['Dynatrace_LIVE'], 'tenant_name': ['tenant1'], 'window_id': ['90916273-5320-410c-b7a0-5548711b52f1'], 'window_name': ['Updated Window'], 'window_planned': ['True'], 'window_description': ['Updated'], 'window_recurrence': ['ONCE'], 'window_day_of_week': [''], 'window_day_of_month': ['1'], 'window_supression': ['DETECT_PROBLEMS_AND_ALERT'], 'window_start_time': [''], 'window_duration': [''], 'window_maintenance_start': ['2019-01-15 23:00'], 'window_maintenance_end': ['2019-01-15 23:05'], 'form-TOTAL_FORMS': ['1'], 'form-INITIAL_FORMS': ['0'], 'form-MIN_NUM_FORMS': ['0'], 'form-MAX_NUM_FORMS': ['10'], 'form-0-entity_type': ['OS'], 'form-0-tags_or_entities': ['TAGS'], 'form-0-filter_value': ['Windows'], 'form-__prefix__-entity_type': [''], 'form-__prefix__-tags_or_entities': [''], 'form-__prefix__-filter_value': ['']})

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json(), 204)

    def test_delete(self):
        mock_server_ex = 'https://' + FULL_SET['Dynatrace_LIVE']['url'] + '/mockserver/expectation'
        data = [{
            "httpRequest" : {
                "method" : "DELETE",
                "path" : "/api/config/v1/maintenanceWindows/90916273-5320-410c-b7a0-5548711b52f1",
                "queryStringParameters" : {
                    "Api-Token" : [ "sample_api_token" ]
                },
            },
            "httpResponse" : {
                "statusCode": 204
            }
        }]
        
        headers = {"Content-Type": "application/json"}
        with no_ssl_verification():
            response = requests.put(mock_server_ex, data=json.dumps(data), verify=False, headers=headers)
          
        
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()

        c = Client()
        c.login(username='testuser', password='12345')

        response = c.post('/maintenance/delete/', {'window_id': ['90916273-5320-410c-b7a0-5548711b52f1'], 'cluster_name': ['Dynatrace_LIVE'], 'tenant_name': ['tenant1']})
        
        self.assertEquals(response.status_code, 200)
        
    def test_get_window_details(self):
        mock_server_ex = 'https://' + FULL_SET['Dynatrace_LIVE']['url'] + '/mockserver/expectation'

        data = [{
            "httpRequest" : {
                "method" : "GET",
                "path" : "/api/config/v1/maintenanceWindows/90916273-5320-410c-b7a0-5548711b52f1",
                "queryStringParameters" : {
                    "Api-Token" : [ "sample_api_token" ]
                }
            },
            "httpResponse" : {
                "body" : {
                    "type": "JSON",
                    "json": {'metadata': {'configurationVersions': [0], 'clusterVersion': '1.192.96.20200507-085711'}, 'id': '90916273-5320-410c-b7a0-5548711b52f1', 'name': 'MockServer2', 'description': 'MockServer', 'type': 'PLANNED', 'suppression': 'DETECT_PROBLEMS_AND_ALERT', 'scope': {'entities': [], 'matches': [{'type': 'OS', 'managementZoneId': None, 'mzId': None, 'tags': [{'context': 'CONTEXTLESS', 'key': 'Windows'}], 'tagCombination': 'OR'}]}, 'schedule': {'recurrenceType': 'ONCE', 'start': '2019-01-15 23:00', 'end': '2019-01-15 23:04', 'zoneId': 'America/Toronto'}}
                }
            }
        }]

        
        headers = {"Content-Type": "application/json"}
        with no_ssl_verification():
            response = requests.put(mock_server_ex, data=json.dumps(data), verify=False, headers=headers)

        

        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()

        c = Client()
        c.login(username='testuser', password='12345')
        response = c.post('/maintenance/get_window_details', {'window_id': ['90916273-5320-410c-b7a0-5548711b52f1'], 'cluster_name': ['Dynatrace_LIVE'], 'tenant_name': ['tenant1']})

        self.assertEquals(response.status_code, 200)
        self.assertIn('metadata', response.json())
        self.assertIn('schedule', response.json())

    def test_get_all_windows(self):

        mock_server_ex = 'https://' + FULL_SET['Dynatrace_LIVE']['url'] + '/mockserver/expectation'

        data = [{
            "httpRequest" : {
                "method" : "GET",
                "path" : "/api/config/v1/maintenanceWindows",
                "queryStringParameters" : {
                    "Api-Token" : [ "sample_api_token" ]
                }
            },
            "httpResponse" : {
                "body" : {
                    "type": "JSON",
                    "json": {'values': [{'id': '727ffd0e-f4d7-4fa1-ab49-169f892a8541', 'name': 'MockServer2', 'description': 'MockServer'}, {'id': '90916273-5320-410c-b7a0-5548711b52f1', 'name': 'Updated Window', 'description': 'Updated'}, {'id': 'a88b3a94-56c3-4dff-be9a-55e04e9a9a00', 'name': 'Window rando', 'description': 'test'}, {'id': 'a7e60299-4567-4774-9c91-450fe075b249', 'name': 'MockServer2', 'description': 'MockServer'}, {'id': '85173510-602c-4180-9efd-7398b7e264e5', 'name': 'WindowRando2', 'description': 'qwerqwer'}, {'id': 'd23b3f77-bd78-4021-a73a-5726212cc2e8', 'name': 'rando tssrsr', 'description': '123213'}, {'id': '610e3652-48f6-47ee-9a70-3ddebd346173', 'name': 'MockServer2', 'description': 'MockServer'}, {'id': 'f1a88e4c-a16e-42f4-a6a5-16cba671b24f', 'name': 'testerino', 'description': 'qwer'}, {'id': 'ca2a120b-d51a-44bc-ac32-193ac959cb7e', 'name': 'testerio', 'description': 'dasdasda'}, {'id': 'c23f490d-a207-4b48-a692-2b5bee943021', 'name': 'rando tssrsr', 'description': '123213'}, {'id': '648449ba-3869-4836-82b9-c2bbcef758dc', 'name': 'MockServer2', 'description': 'MockServer'}, {'id': 'b77383ce-fc00-4307-8f07-11f745b5b09f', 'name': 'Window rando', 'description': 'test'}, {'id': 'ba99fa4f-a768-4d72-a07b-c248e6223992', 'name': 'Window rando', 'description': 'test'}, {'id': '7ce307fc-c04e-4766-ad2d-42cc53c44e2c', 'name': 'Window rando', 'description': 'test'}, {'id': '2bcca51e-8382-468e-9554-99f88d4db9cd', 'name': 'First Window', 'description': 'Act 1 Scene 1'}, {'id': '477febe8-7340-4b86-a2e9-6e4c43d6fb25', 'name': 'Window rando', 'description': 'test'}, {'id': '8d3e7c6e-c412-426c-b927-02803c5bf12d', 'name': 'Updated Window2', 'description': 'UpdatedWindowed'}, {'id': '04f21b98-10a3-4e4b-9c93-112060f0a521', 'name': 'WindowRando2', 'description': 'qwerqwer'}, {'id': '9607bd47-bb7b-4663-94ee-321bb9d17415', 'name': 'Window rando', 'description': 'test'}, {'id': '9fb1c6d6-ff0e-44ef-b095-0347811d98a8', 'name': 'Window rando', 'description': 'test'}, {'id': '0bdde800-c05f-4dcd-bcdb-660bf737552e', 'name': 'Window rando', 'description': 'test'}, {'id': '8787b034-a696-4953-bb4b-ba922c823d50', 'name': 'Window rando', 'description': 'test'}, {'id': '059baa16-79a4-4500-9ed8-5dee700330c6', 'name': 'MockServer2', 'description': 'MockServer'}, {'id': '45390624-bdda-4eb4-bceb-915308571616', 'name': 'Window rando', 'description': 'test'}, {'id': 'fbf857ad-2d7a-4c72-bb36-6fce91cfb784', 'name': 'MockServer2', 'description': 'MockServer'}, {'id': 'b67afe69-b14f-478b-b1a9-ff5360d1a4ea', 'name': 'MockServer2', 'description': 'MockServer'}, {'id': '9d0e414d-8316-4cc5-96c0-9f0084227dce', 'name': 'Window rando', 'description': 'test'}, {'id': '36baa734-b8fa-481a-a793-cbbe0c7058fc', 'name': 'WindowRando2', 'description': 'qwerqwer'}, {'id': '86149f14-282d-4b63-8ca9-0aba9ffb90ba', 'name': 'MackServer', 'description': 'MockServer'}, {'id': '8141cc8f-939b-422e-a834-2456f32865ee', 'name': 'rando tssrsr', 'description': '123213'}, {'id': 'dc7526c0-877a-4b13-b278-4743c7d0b9f6', 'name': 'MackServer', 'description': 'MockServer'}, {'id': 'bd45b57c-753d-41a4-b261-30f25a49b6e2', 'name': 'WindowRando2', 'description': 'qwerqwer'}, {'id': '8d3e7c6e-c412-426c-b927-2803c5bf12db', 'name': 'Updated Please', 'description': 'updated'}, {'id': 'e1d70333-9fec-45b3-bcc3-845b9753dea5', 'name': 'WindowRando2', 'description': 'qwerqwer'}, {'id': 'd49bee6d-3b3c-430a-bbeb-acffb4cf3402', 'name': 'Window rando', 'description': 'test'}, {'id': '1f47b301-b309-4b26-9ed2-e15ffceba931', 'name': 'Window rando', 'description': 'test'}, {'id': '4a9121c8-c186-412d-b28e-7379c04745a6', 'name': 'Window rando', 'description': 'test'}, {'id': 'cda8587b-ab87-4e49-a151-349eac9c5228', 'name': 'Window rando', 'description': 'test'}, {'id': '5eb8e489-0552-4639-94ec-c2df7b2e1ed8', 'name': 'Window rando', 'description': 'test'}, {'id': 'e5dd513e-f594-4a93-8b5b-6c0a573e5933', 'name': 'Window rando', 'description': 'test'}, {'id': '367bb6f3-fc3d-4f32-86ac-24131505fa07', 'name': 'testerino', 'description': 'qwer'}, {'id': '3080f51d-40d9-428e-8aa6-9645233ac742', 'name': 'Window rando', 'description': 'test'}, {'id': '70992491-f0f6-4944-9480-1378eecf57d3', 'name': 'rando tssrsr', 'description': '123213'}]}
                }
            }
        }]

        
        headers = {"Content-Type": "application/json"}
        with no_ssl_verification():
            response = requests.put(mock_server_ex, data=json.dumps(data), verify=False, headers=headers)

        

        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()

        c = Client()
        c.login(username='testuser', password='12345')
        response = c.post('/maintenance/get_all_windows', {'csrfmiddlewaretoken': ['2THLYNQ0rTm2xXfprBD6XQkwSHcfGNkXDAUBvh5OQNbhAlZOL52d23x128aF9hOM'], 'cluster_name': ['Dynatrace_LIVE'], 'tenant_name': ['tenant1']})

        self.assertEquals(response.status_code, 200)
        self.assertIn('values', response.json())

