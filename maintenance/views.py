from django.http import HttpResponseRedirect
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from django.shortcuts import render

from .forms import create_maintenance_window
from .forms import view_maintenance_window
from .forms import update_maintenance_window
from .forms import filter_set
from .process_window import create_filters_from_formset

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

# Create your views here.
def update(request):

    form = update_maintenance_window()
    formset = filter_set
    return render(
            request,
            'maintenance/update.html',
            {
                    'form': form,
                    'formset': formset
            }
    )

def submit_create(request):
    """Submit Maintenance Window info to Cluster/Tenant Combo"""
    if request.method == "POST":
        if request.is_ajax():
            form = create_maintenance_window(request.POST)
            # print(request.POST)
            if form.is_valid():
                #Popping all the args to get strip the information to a valid formset
                post_args = request.POST.copy()
                day = None
                if 'window_day_of_week' in post_args:
                    day = post_args.pop ('window_day_of_week')
                if 'window_day_of_month' in post_args:
                    day = post_args.pop ('window_day_of_month')

                schedule = maintenance.generate_schedule (
                        post_args.pop ('window_recurrence')[0],
                        post_args.pop ('window_start_time')[0],
                        post_args.pop ('window_duration')[0],
                        post_args.pop ('window_maintenance_start')[0],
                        post_args.pop ('window_maintenance_end')[0],
                        day
                )

                maintenance_window_name = post_args.pop ('window_name')[0]
                maintenance_window_desc = post_args.pop ('window_description')[0]
                maintenance_window_supp = post_args.pop ('window_supression')[0]
                maintenance_window_plan = post_args.pop ('window_planned')[0]
                cluster_name = post_args.pop ('cluster_name')[0]
                tenant_name = post_args.pop ('tenant_name')[0]
                post_args.pop('csrfmiddlewaretoken')
                
                formset = filter_set(post_args)
                scope = None
                print("Formset: " + str(formset.is_valid()))
                if formset.is_valid():
                    scope = create_filters_from_formset (formset)

                payload = maintenance.generate_window_json (
                        maintenance_window_name,
                        maintenance_window_desc,
                        maintenance_window_supp,
                        schedule,
                        is_planned=maintenance_window_plan,
                        scope=scope
                )

                try:
                    new_window = maintenance.create_window(
                            uv.FULL_SET[cluster_name],
                            tenant_name,
                            payload
                    )
                    return JsonResponse (new_window, safe=False)
                except Exception as e:
                    print (e)
                    # return HttpResponseBadRequest(e)
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
        return JsonResponse(list_of_windows)
    return HttpResponseBadRequest ("Invalid!")