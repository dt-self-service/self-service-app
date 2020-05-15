from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from django.shortcuts import render
from sso.validate import is_member_of_group

from .forms import create_maintenance_window
from .forms import view_maintenance_window
from .forms import update_maintenance_window
from .forms import filter_set
from .process_window import create_filters_from_formset
from .process_window import parse_submit_form

from dynatrace.tenant import maintenance
import user_variables as uv
from dynatrace.requests import request_handler as rh

# Create your views here.


def create(request):
  # is_member_of_group(request, 'Maintenance Writer')
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
  # is_member_of_group(request, 'Maintenance Viewer')
  if request.method == "POST":
    form = view_maintenance_window(request.POST)
    cluster = uv.FULL_SET[request.POST['cluster_name']]
    list_of_windows = maintenance.get_windows(
        cluster, request.POST['tenant_name'])
  else:
    form = view_maintenance_window()
    # Hard Coded for now, Philly will add logic
    list_of_windows = {'values': {}}
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
  """Update Page for Maintenance Window"""
  # is_member_of_group(request, 'Maintenance Writer')
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


def delete(request):
  """Delete AJAX for Maintenance Window"""
  # is_member_of_group(request, 'Maintenance Writer')
  if request.method == "POST":
    cluster = request.POST['cluster_name']
    tenant = request.POST['tenant_name']
    window_id = request.POST['window_id']

    print (cluster, tenant, window_id)
    response = rh.config_delete(cluster, tenant, '/maintenanceWindows/' + window_id)
    print (response.url)

    window_details = maintenance.delete_window(
        uv.FULL_SET[cluster], tenant, window_id)
    if window_details == 204:
      return HttpResponse("Success")
  return HttpResponseBadRequest("Invalid!")


def submit_create(request):
  """Submit Maintenance Window info to Cluster/Tenant Combo"""
  # is_member_of_group(request, 'Maintenance Writer')
  if request.method == "POST":
    form = create_maintenance_window(request.POST)
    if form.is_valid():
      # Popping all the args to get strip the information to a valid formset

      cluster_name = request.POST['cluster_name']
      tenant_name = request.POST['tenant_name']
      payload = parse_submit_form(request.POST.copy())

      try:
        new_window = maintenance.create_window(
            uv.FULL_SET[cluster_name],
            tenant_name,
            payload
        )
        return JsonResponse(new_window, safe=False)
      except Exception as e:
        print(e)
        # return HttpResponseBadRequest(e)
    else:
      print("Invalid Form!")
      return HttpResponseBadRequest("Invalid Form!")
  return HttpResponseBadRequest("Invalid Protocol")


def submit_update(request):
  """Submit Maintenance Window info to Cluster/Tenant Combo"""
  # is_member_of_group(request, 'Maintenance Writer')
  if request.method == "POST":
    form = update_maintenance_window(request.POST)
    # print(request.POST)
    if form.is_valid():
      # Popping all the args to get strip the information to a valid formset
      post_data = request.POST.copy()
      window_id = post_data.pop('window_id')[0]
      cluster_name = request.POST['cluster_name']
      tenant_name = request.POST['tenant_name']
      payload = parse_submit_form(post_data)
      try:
        #print(payload)
        update_window = maintenance.update_window(
            uv.FULL_SET[cluster_name],
            tenant_name,
            window_id,
            payload
        )
        return JsonResponse(update_window, safe=False)
      except Exception as e:
        print(e)
        # return HttpResponseBadRequest(e)
    else:
      print("Invalid Form!")
      return HttpResponseBadRequest("Invalid Form!")
  return HttpResponseBadRequest("Invalid Protocol")


def get_window_details(request):
  """Extract Maintenance Window Information"""
  # is_member_of_group(request, 'Maintenance Writer')
  if request.method == "POST":
    cluster = request.POST['cluster_name']
    tenant = request.POST['tenant_name']
    window_id = request.POST['window_id']

    window_details = maintenance.get_window(
        uv.FULL_SET[cluster], tenant, window_id)
    return JsonResponse(window_details)
  return HttpResponseBadRequest("Invalid!")


def get_all_windows(request):
  # is_member_of_group(request, 'Maintenance Writer')
  if request.method == 'POST':
    # form = view_maintenance_window(request.POST)
    cluster = uv.FULL_SET[request.POST['cluster_name']]
    
    list_of_windows = maintenance.get_windows(
        cluster, request.POST['tenant_name'])
    return JsonResponse(list_of_windows)
  return HttpResponseBadRequest("Invalid!")
