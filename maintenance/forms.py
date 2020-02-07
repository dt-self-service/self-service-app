from django import forms

SUPPRESSION_TYPES = [
        ("DETECT_PROBLEMS_AND_ALERT", "Detect problems and alert"), 
        ("DETECT_PROBLEMS_DONT_ALERT", "Detect problems but don't alert"), 
        ("DONT_DETECT_PROBLEMS", "Disable problem detection during maintenance")
]
PLANNED_TYPES = [
        ("PLANNED", "PLANNED"), 
        ("UNPLANNED", "UNPLANNED")
]
RECURRENCE_TYPES = ["Daily", "Day of week", "Day of Month", "Once only"]

class create_maintenance_window(forms.Form):
    
    window_name = forms.CharField(label="Maintenance Window Name", max_length=100)
    window_planned = forms.ChoiceField(choices=PLANNED_TYPES)
    window_description = forms.CharField(label='Description', max_length=200)
    #window_recurrence = forms.ChoiceField(choices=RECURRENCE_TYPES)
    window_supression = forms.ChoiceField(choices=SUPPRESSION_TYPES)
    window_maintenance_start = forms.CharField(label="Maintenance Start", max_length=16)
    window_maintenance_end = forms.CharField(label="Maintenance End", max_length=16)
    