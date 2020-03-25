from django import forms
from django.forms import formset_factory
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

CLUSTER_LIST = [("", "Choose Cluster")]
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


AVAILABLE_FILTER_FIELDS = [
        ("", "Entity Filter (Optional)"),
        ("APPLICATION", "Application"),
        ("APPLICATION_METHOD", "Application Method"),
        ("APPLICATION_METHOD_GROUP", "Application Method Group"),
        ("AUTO_SCALING_GROUP", "Auto Scaling Group"),
        ("AUXILIARY_SYNTHETIC_TEST", "Auxiliary Synthetic Test"),
        ("AWS_APPLICATION_LOAD_BALANCER", "AWS Application Load Balancer"),
        ("AWS_AVAILABILITY_ZONE", "AWS Availability Zone"),
        ("AWS_CREDENTIALS", "AWS Credentials"),
        ("AWS_LAMBDA_FUNCTION", "AWS Lambda Function"),
        ("AWS_NETWORK_LOAD_BALANCER", "AWS Network Load Balancer"),
        ("AZURE_API_MANAGEMENT_SERVICE", "Azure Api Management Service"),
        ("AZURE_APPLICATION_GATEWAY", "Azure Application Gateway"),
        ("AZURE_COSMOS_DB", "Azure Cosmos DB"),
        ("AZURE_CREDENTIALS", "Azure Credentials"),
        ("AZURE_EVENT_HUB", "Azure Event Hub"),
        ("AZURE_EVENT_HUB_NAMESPACE", "Azure Event Hub Namespace"),
        ("AZURE_FUNCTION_APP", "Azure Function App"),
        ("AZURE_IOT_HUB", "Azure Iot Hub"),
        ("AZURE_LOAD_BALANCER", "Azure Load Balancer"),
        ("AZURE_MGMT_GROUP", "Azure Mgmt Group"),
        ("AZURE_REDIS_CACHE", "Azure Redis Cache"),
        ("AZURE_REGION", "Azure Region"),
        ("AZURE_SERVICE_BUS_NAMESPACE", "Azure Service Bus Namespace"),
        ("AZURE_SERVICE_BUS_QUEUE", "Azure Service Bus Queue"),
        ("AZURE_SERVICE_BUS_TOPIC", "Azure Service Bus Topic"),
        ("AZURE_SQL_DATABASE", "Azure Sql Database"),
        ("AZURE_SQL_ELASTIC_POOL", "Azure Sql Elastic Pool"),
        ("AZURE_SQL_SERVER", "Azure Sql Server"),
        ("AZURE_STORAGE_ACCOUNT", "Azure Storage Account"),
        ("AZURE_SUBSCRIPTION", "Azure Subscription"),
        ("AZURE_TENANT", "Azure Tenant"),
        ("AZURE_VM", "Azure VM"),
        ("AZURE_VM_SCALE_SET", "Azure VM Scale Set"),
        ("AZURE_WEB_APP", "Azure Web App"),
        ("CF_APPLICATION", "CF Application"),
        ("CF_FOUNDATION", "CF Foundation"),
        ("CINDER_VOLUME", "Cinder Volume"),
        ("CUSTOM_APPLICATION", "Custom Application"),
        ("CUSTOM_DEVICE", "Custom Device"),
        ("CUSTOM_DEVICE_GROUP", "Custom Device Group"),
        ("DCRUM_APPLICATION", "Dcrum Application"),
        ("DCRUM_SERVICE", "Dcrum Service"),
        ("DCRUM_SERVICE_INSTANCE", "Dcrum Service Instance"),
        ("DEVICE_APPLICATION_METHOD", "Device Application Method"),
        ("DISK", "Disk"),
        ("DOCKER_CONTAINER_GROUP_INSTANCE", "Docker Container Group Instance"),
        ("DYNAMO_DB_TABLE", "Dynamo DB Table"),
        ("EBS_VOLUME", "Ebs Volume"),
        ("EC2_INSTANCE", "Ec2 Instance"),
        ("ELASTIC_LOAD_BALANCER", "Elastic Load Balancer"),
        ("ENVIRONMENT", "Environment"),
        ("EXTERNAL_SYNTHETIC_TEST_STEP", "External Synthetic Test Step"),
        ("GCP_ZONE", "GCP Zone"),
        ("GEOLOCATION", "Geolocation"),
        ("GEOLOC_SITE", "Geoloc Site"),
        ("GOOGLE_COMPUTE_ENGINE", "Google Compute Engine"),
        ("HOST", "Host"),
        ("HOST_GROUP", "Host Group"),
        ("HTTP_CHECK", "Http Check"),
        ("HTTP_CHECK_STEP", "Http Check Step"),
        ("HYPERVISOR", "Hypervisor"),
        ("KUBERNETES_CLUSTER", "Kubernetes Cluster"),
        ("KUBERNETES_NODE", "Kubernetes Node"),
        ("MOBILE_APPLICATION", "Mobile Application"),
        ("NETWORK_INTERFACE", "Network Interface"),
        ("NEUTRON_SUBNET", "Neutron Subnet"),
        ("OPENSTACK_PROJECT", "Openstack Project"),
        ("OPENSTACK_REGION", "Openstack Region"),
        ("OPENSTACK_VM", "Openstack VM"),
        ("OS", "OS"),
        ("PROCESS_GROUP", "Process Group"),
        ("PROCESS_GROUP_INSTANCE", "Process Group Instance"),
        ("RELATIONAL_DATABASE_SERVICE", "Relational Database Service"),
        ("SERVICE", "Service"),
        ("SERVICE_INSTANCE", "Service Instance"),
        ("SERVICE_METHOD", "Service Method"),
        ("SERVICE_METHOD_GROUP", "Service Method Group"),
        ("SWIFT_CONTAINER", "Swift Container"),
        ("SYNTHETIC_LOCATION", "Synthetic Location"),
        ("SYNTHETIC_TEST", "Synthetic Test"),
        ("SYNTHETIC_TEST_STEP", "Synthetic Test Step"),
        ("VIRTUALMACHINE", "Virtualmachine"),
        ("VMWARE_DATACENTER", "VMware Datacenter"),
]

TAGS_OR_ENTITIES_CHOICE = [
        ("","Filter Type"),
        ("TAGS","Tags"),
        ("ENTITIES","Entities"),
]

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
            widget=forms.Select(
                attrs={'class': 'btn btn-secondary dropdown-toggle col-lg-4 col-sm-12 col-md-8'}
            )
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
                    attrs={'class': 'form-control btn btn-secondary dropdown-toggle col-lg-4 col-sm-12 col-md-8'}
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

class update_maintenance_window(forms.Form):
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
            widget=forms.Select(
                attrs={'class': 'btn btn-secondary dropdown-toggle col-lg-4 col-sm-12 col-md-8'}
            )
    )
    window_id = forms.CharField(
            label="Maintenance Window ID",
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
                    attrs={'class': 'form-control btn btn-secondary dropdown-toggle col-lg-4 col-sm-12 col-md-8'}
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

class view_maintenance_window(forms.Form):
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
            widget=forms.Select(
                attrs={'class': 'btn btn-secondary dropdown-toggle col-lg-4 col-sm-12 col-md-8'}
            )
    )

class window_filters(forms.Form):

        entity_type = forms.ChoiceField(
                label = "",
                choices = AVAILABLE_FILTER_FIELDS,
                widget=forms.Select(
                        attrs={'class': 'btn btn-secondary dropdown-toggle col-lg-2 col-sm-12 col-md-8'}
                )
        )
        tags_or_entities = forms.ChoiceField(
                label = "",
                choices = TAGS_OR_ENTITIES_CHOICE,
                widget=forms.Select(
                        attrs={'class': 'btn btn-secondary dropdown-toggle col-lg-2 col-sm-12 col-md-8'}
                )
        )
        filter_value = forms.CharField(
                label = "",
                max_length=100,
                widget=forms.TextInput(
                        attrs={'class': 'form-control col-lg-6 col-sm-12 col-md-8','placeholder': 'Separated By ";"'}
                )
        )

filter_set = formset_factory(window_filters, extra=1, max_num=10)