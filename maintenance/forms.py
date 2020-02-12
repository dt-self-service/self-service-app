from django import forms
from django.utils import timezone
import user_variables as uv

SUPPRESSION_TYPES = [
        ("DETECT_PROBLEMS_AND_ALERT", "Detect problems and alert"), 
        ("DETECT_PROBLEMS_DONT_ALERT", "Detect problems but don't alert"), 
        ("DONT_DETECT_PROBLEMS", "Disable problem detection during maintenance")
]
PLANNED_TYPES = [
        (True, "PLANNED"), 
        (False, "UNPLANNED")
]
RECURRENCE_TYPES = [
        ("ONCE", "Once only"),
        ("DAILY", "Daily"),
        ("WEEKLY", "Day of week"),
        ("MONTHLY","Day of month"),
]

CLUSTER_LIST = []
for cluster in uv.FULL_SET:
    CLUSTER_LIST.append((cluster, cluster))

DAYS_OF_WEEK = [
        ("", "Choose Day"),
        ("SUNDAY", "Sunday"),
        ("MONDAY", "Monday"),
        ("TUESDAY", "Tuesday"),
        ("WEDNESDAY", "Wednesday"),
        ("THURSDAY", "Thursday"),
        ("FRIDAY", "Friday"),
        ("SATURDAY", "Saturday"),
]

DAYS_OF_MONTH = []
for i in range(31):
    DAYS_OF_MONTH.append((i+1, i+1))

class create_maintenance_window(forms.Form):
    cluster_name = forms.ChoiceField(
            label="Cluster Name", 
            choices=CLUSTER_LIST,
            widget=forms.Select(
                    attrs={'class': 'btn btn-secondary dropdown-toggle'}
            )
    )
    tenant_name = forms.CharField(label="Tenant Name", max_length=100)
    tags_list = forms.CharField(label="Tag List (Comma Seperated)", required=False)
    management_zone_name = forms.CharField(label="Management Zone ID", required=False, max_length=100)
    window_name = forms.CharField(label="Maintenance Window Name", max_length=100)
    window_planned = forms.ChoiceField(choices=PLANNED_TYPES)
    window_description = forms.CharField(label='Description', max_length=200)
    window_recurrence = forms.ChoiceField(choices=RECURRENCE_TYPES)
    window_day_of_week = forms.ChoiceField(choices=DAYS_OF_WEEK, required=False)
    window_day_of_month = forms.ChoiceField(choices=DAYS_OF_MONTH, required=False)
    window_supression = forms.ChoiceField(choices=SUPPRESSION_TYPES)
    window_start_time = forms.TimeField(label='Window Start Time', input_formats=["%H:%M"], required=False)
    window_duration = forms.IntegerField(label='Window Duration (in Minutes)', required=False)
    window_maintenance_start = forms.DateField(label="Maintenance Start (Format Example: 2019-01-15 23:00)", input_formats= ['%Y-%m-%d %H:%M'])
    window_maintenance_end = forms.DateField(label="Maintenance End (Format Example: 2019-01-15 23:00)", input_formats= ['%Y-%m-%d %H:%M'])
    
    def fields_required(self, fields):
        #    """Used for conditionally marking fields as required."""
        for field in fields:
            if not self.cleaned_data.get(field, ''):
                msg = forms.ValidationError("This field is required.")
                self.add_error(field, msg)

    def clean(self):
        recurrence = self.cleaned_data.get('window_recurrence')

        if recurrence != "ONCE":
            self.fields_required(['window_start_time'])
            self.fields_required(['window_duration'])
        else:
            self.cleaned_data['window_start_time'] = None
            self.cleaned_data['window_duration'] = None

        if recurrence == "WEEKLY":
            self.fields_required(['window_day_of_week'])
        else:
            self.cleaned_data['window_day_of_week'] = None

        if recurrence == "MONTHLY":
            self.fields_required(['window_day_of_month'])
        else:
            self.cleaned_data['window_day_of_month'] = None

        return self.cleaned_data
    
    