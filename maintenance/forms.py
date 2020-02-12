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
                    attrs={'class': 'btn btn-secondary dropdown-toggle col-lg-4 col-sm-12 col-md-8'}
            )
    )
    tenant_name = forms.CharField(
            label="Tenant Name",
            max_length=100,
            widget=forms.TextInput(attrs={'class': 'form-control col-lg-4 col-sm-12 col-md-8'})
    )
    window_name = forms.CharField(
            label="Maintenance Window Name",
            max_length=100,
            widget=forms.TextInput(attrs={'class': 'form-control col-lg-4 col-sm-12 col-md-8'})
    )
    window_planned = forms.ChoiceField(
            choices=PLANNED_TYPES,
            widget=forms.Select(
                    attrs={'class': 'btn btn-secondary dropdown-toggle col-lg-4 col-sm-12 col-md-8'}
            )
    )
    window_description = forms.CharField(
            label='Description',
            max_length=200,
            widget=forms.TextInput(attrs={'class': 'form-control col-lg-4 col-sm-12 col-md-8'})
    )
    window_recurrence = forms.ChoiceField(
            choices=RECURRENCE_TYPES,
            widget=forms.Select(
                    attrs={'class': 'btn btn-secondary dropdown-toggle col-lg-4 col-sm-12 col-md-8'}
            )
    )
    window_day_of_week = forms.ChoiceField(
            choices=DAYS_OF_WEEK,
            required=False,
            widget=forms.Select(
                    attrs={'class': 'btn btn-secondary dropdown-toggle col-lg-4 col-sm-12 col-md-8'}
            )
    )
    window_day_of_month = forms.ChoiceField(
            choices=DAYS_OF_MONTH,
            required=False,
            widget=forms.Select(
                    attrs={'class': 'form-control btn btn-secondary dropdown-toggle col-lg-4 col-sm-12 col-md-8 col-'}
            )
    )
    window_supression = forms.ChoiceField(
            choices=SUPPRESSION_TYPES,
            widget=forms.Select(
                    attrs={'class': 'btn btn-secondary dropdown-toggle col-lg-4 col-sm-12 col-md-8'}
            )
    )
    window_start_time = forms.TimeField(
            label='Window Start Time',
            input_formats=["%H:%M"],
            required=False,
            widget=forms.TimeInput(attrs={'class': 'form-control col-lg-4 col-sm-12 col-md-8'})
    )
    window_duration = forms.IntegerField(
            label='Window Duration (in Minutes)',
            required=False,
            widget=forms.TextInput(attrs={'class': 'form-control col-lg-4 col-sm-12 col-md-8'})
    )
    window_maintenance_start = forms.DateField(
            label="Maintenance Start (Format Example: 2019-01-15 23:00)",
            input_formats= ['%Y-%m-%d %H:%M'],
            widget=forms.DateInput(attrs={'class': 'form-control col-lg-4 col-sm-12 col-md-8'})
    )
    window_maintenance_end = forms.DateField(
            label="Maintenance End (Format Example: 2019-01-15 23:00)",
            input_formats= ['%Y-%m-%d %H:%M'],
            widget=forms.TextInput(attrs={'class': 'form-control col-lg-4 col-sm-12 col-md-8'})
    )
    window_add_filters = forms.BooleanField(
            widget=forms.CheckboxInput(attrs={'class': 'form-check'}),
            required=False,
    )
    tags_list = forms.CharField(
            label="Tag List (Comma Seperated)",
            required=False,
            widget=forms.TextInput(attrs={'class': 'form-control col-lg-4 col-sm-12 col-md-8'})
    )
    management_zone_name = forms.CharField(
            label="Management Zone ID",
            required=False,
            max_length=100,
            widget=forms.TextInput(attrs={'class': 'form-control col-lg-4 col-sm-12 col-md-8'})
    )
    


    def fields_required(self, fields):
        #    """Used for conditionally marking fields as required."""
        for field in fields:
            if not self.cleaned_data.get(field, ''):
                msg = forms.ValidationError("This field is required.")
                self.add_error(field, msg)

    def clean(self):
        recurrence = self.cleaned_data.get('window_recurrence')
        filtering = self.cleaned_data.get('window_add_filters')

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

        if filtering:
            self.fields_required(['tags_list'])
        else:
            self.cleaned_data['tags_list'] = None

        return self.cleaned_data
    
    