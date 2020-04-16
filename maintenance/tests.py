from django.test import TestCase
from maintenance import process_window

# Create your tests here.


class MaintenanceTests(TestCase):
  def process_windows_basic(self):
    test_args = {
        'csrfmiddlewaretoken': ['053VyQSDnT2KLWFRzeSaYpw9h1gVQrNxoHhy4HaQN3VxS8pGLbOOwkHNS2Ok5Pc5'],
        'cluster_name': ['Sprint'],
        'tenant_name': ['single'],
        'window_name': ['Window 10'],
        'window_planned': ['True'],
        'window_description': ['Test Window for demonstration'],
        'window_recurrence': ['ONCE'],
        'window_day_of_week': [''],
        'window_day_of_month': ['1'],
        'window_supression': ['DETECT_PROBLEMS_AND_ALERT'],
        'window_start_time': [''],
        'window_duration': [''],
        'window_maintenance_start': ['2019-01-15 23:00'],
        'window_maintenance_end': ['2019-01-15 23:50'],
        'form-TOTAL_FORMS': ['1'],
        'form-INITIAL_FORMS': ['0'],
        'form-MIN_NUM_FORMS': ['0'],
        'form-MAX_NUM_FORMS': ['10'],
        'form-0-entity_type': ['AZURE_EVENT_HUB_NAMESPACE'],
        'form-0-tags_or_entities': ['TAGS'],
        'form-0-filter_value': ['asdfasdf'],
        'form-__prefix__-entity_type': [''],
        'form-__prefix__-tags_or_entities': [''],
        'form-__prefix__-filter_value': ['']
    }
    actual_payload = process_window.parse_submit_form(test_args)
    expected_payload = {
        'name': 'Window 10',
        'description': 'Test Window for demonstration',
        'suppression': 'DETECT_PROBLEMS_AND_ALERT',
        'schedule': {
            'recurrenceType': 'ONCE',
            'start': '2019-01-15 23:00',
            'end': '2019-01-15 23:50',
            'zoneId': 'America/Chicago'
        },
        'type': 'PLANNED',
        'scope': {
            'entities': [],
            'matches': [
                {
                    'type': 'AZURE_EVENT_HUB_NAMESPACE',
                    'managementZoneId': 'null',
                    'tags': [
                        {
                            'context': 'CONTEXTLESS',
                            'key': 'asdfasdf'
                        }
                    ]
                }
            ]
        }
    }
    self.assertEqual(actual_payload, expected_payload)

