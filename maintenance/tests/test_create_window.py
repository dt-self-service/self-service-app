from django.test import TestCase
from django.http import QueryDict

from maintenance import process_window

# Create your tests here.
class MaintenanceTests(TestCase):
  def test_create_windows(self):
    args_dict = {'csrfmiddlewaretoken': 'D1kSK7nV75ZN5jQ2pvdwkiJUCEFKj2cXyP4Aji4lsaOMKuyAm0Jg45Vk89S5bTzg', 
        'cluster_name': 'Dynatrace_LIVE',
        'tenant_name': 'tenant1', 
        'window_name': 'Window rando', 
        'window_planned': 'True', 
        'window_description': 'test', 
        'window_recurrence': 'ONCE', 
        'window_day_of_week': '', 
        'window_day_of_month': '1', 
        'window_supression': 'DETECT_PROBLEMS_AND_ALERT', 
        'window_start_time': '', 
        'window_duration': '', 
        'window_maintenance_start': '2020-09-09 11:00', 
        'window_maintenance_end': '2020-09-09 11:30', 
        'form-TOTAL_FORMS': '1', 
        'form-INITIAL_FORMS': '0', 
        'form-MIN_NUM_FORMS': '0', 
        'form-MAX_NUM_FORMS': '10', 
        'form-0-entity_type': 'OS', 
        'form-0-tags_or_entities': 'TAGS', 
        'form-0-filter_value': 'Windows', 
        'form-__prefix__-entity_type': '', 
        'form-__prefix__-tags_or_entities': '', 
        'form-__prefix__-filter_value': ''
    }

    query_dict = QueryDict('', mutable=True)
    query_dict.update(args_dict)


    actual_payload = process_window.parse_submit_form(query_dict)
    
    expected_payload = {'name': 'Window rando', 'description': 'test', 'suppression': 'DETECT_PROBLEMS_AND_ALERT', 'schedule': {'recurrenceType': 'ONCE', 'start': '2020-09-09 11:00', 'end': '2020-09-09 11:30', 'zoneId': 'America/Toronto'}, 'type': 'PLANNED', 'scope': {'entities': [], 'matches': [{'type': 'OS', 'managementZoneId': 'null', 'tags': [{'context': 'CONTEXTLESS', 'key': 'Windows'}]}]}}
    self.assertEqual(actual_payload, expected_payload)



