from django.http import HttpResponseRedirect
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from django.shortcuts import render

from .forms import create_maintenance_window
from .forms import view_maintenance_window
from .forms import filter_set
from dynatrace.tenant import maintenance
import user_variables as uv

import json # testing purposes

# Create your views here.
def create(request):

    form = create_maintenance_window()
    formset = filter_set
    return render(
            request,
            'maintenance/create.html',
            {
                    'form': form,
                    'formset': formset
            }
    )

def view(request):
    if request.method == "POST":
            form = view_maintenance_window(request.POST)
            cluster = uv.FULL_SET[request.POST['cluster_name']]
            list_of_windows = maintenance.get_windows(cluster, request.POST['tenant_name'])
    else:
        form = view_maintenance_window()
        list_of_windows = {'values':{}} # Hard Coded for now, Philly will add logic
    return render(
            request,
            'maintenance/view.html',
            {
                    'form': form,
                    'list_of_windows': list_of_windows["values"]
            }
    )

def submit_create(request):
    """Submit Maintenance Window info to Cluster/Tenant Combo"""
    if request.method == "POST":
        if request.is_ajax():
            print ("ajax")
            form = create_maintenance_window(request.POST)
            print(request.POST)
            if form.is_valid():
            # scope = maintenance.generate_scope(
            #     management_zone_id=str(request.POST['management_zone_name'])
            # )

                schedule = maintenance.generate_schedule (
                        request.POST['window_recurrence'],
                        request.POST['window_start_time'],
                        request.POST['window_duration'],
                        request.POST['window_maintenance_start'],
                        request.POST['window_maintenance_end'],
                        day= request.POST['window_day_of_week'] \
                                if request.POST['window_day_of_week'] \
                                else request.POST['window_day_of_month']
                )

                payload = maintenance.generate_window_json (
                        request.POST['window_name'],
                        request.POST['window_description'],
                        request.POST['window_supression'],
                        schedule,
                        is_planned=request.POST['window_planned']
                )
                try:
                    new_window = maintenance.create_window(
                            uv.FULL_SET[request.POST['cluster_name']],
                            request.POST['tenant_name'],
                            payload
                    )
                    return JsonResponse (new_window, safe=False)
                except Exception as e:
                    print (e)
            else:
                print("Invalid Form!")
                return HttpResponseBadRequest("Invalid Form!")
            print ("not ajax")
            return HttpResponseBadRequest("Invalid Call!")
    return HttpResponseBadRequest ("Invalid Protocol")

def fill_maintenance_field(form, window, form_field_name, window_field_name, required=True):
    if window_field_name in window:
        form[form_field_name].initial(window[window_field_name])
        form[form_field_name].disabled = True
    else:
        if required:
            raise Exception ("Required Field Missing!")

def get_window_details(request):
    """Extract Maintenance Window Information"""
    if request.method == "POST" and request.is_ajax():
        cluster = request.POST['cluster_name']
        tenant = request.POST['tenant_name']
        window_id = request.POST['window_id']

        window_details = maintenance.get_window (uv.FULL_SET[cluster], tenant, window_id)
        return JsonResponse (window_details)
    return HttpResponseBadRequest ("Invalid!")

def get_all_windows(request):
    if request.method == 'POST' and request.is_ajax():
        form = view_maintenance_window(request.POST)
        cluster = uv.FULL_SET[request.POST['cluster_name']]
        list_of_windows = maintenance.get_windows(cluster, request.POST['tenant_name'])
        print(list_of_windows)
        return JsonResponse(list_of_windows)
    return HttpResponseBadRequest ("Invalid!")