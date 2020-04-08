from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseForbidden
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from django.shortcuts import render
from auth.validate import is_general_user

from .forms import create_maintenance_window
from .forms import view_maintenance_window
from .forms import update_maintenance_window
from .forms import filter_set
from .process_window import create_filters_from_formset
from .process_window import parse_submit_form

from dynatrace.tenant import maintenance
import user_variables as uv

# Create your views here.


def create(request):
  is_general_user(request)
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
  is_general_user(request)
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
  is_general_user(request)
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

def delete (request):
  """Delete AJAX for Maintenance Window"""
  is_general_user(request)
  if request.method == "POST" and request.is_ajax():
    cluster = request.POST['cluster_name']
    tenant = request.POST['tenant_name']
    window_id = request.POST['window_id']

    window_details = maintenance.delete_window(uv.FULL_SET[cluster], tenant, window_id)
    if window_details == 204:
      return HttpResponse("Success")
  return HttpResponseBadRequest("Invalid!")


def submit_create(request):
  """Submit Maintenance Window info to Cluster/Tenant Combo"""
  is_general_user(request)
  if request.method == "POST":
    if request.is_ajax():
      form = create_maintenance_window(request.POST)
      # print(request.POST)
      if form.is_valid():
        # Popping all the args to get strip the information to a valid formset

        cluster_name = request.POST['cluster_name']
        tenant_name = request.POST['tenant_name']
        payload = parse_submit_form(request.POST.copy())

        try:
          print(payload)
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
      print("not ajax")
      return HttpResponseBadRequest("Invalid Call!")
  return HttpResponseBadRequest("Invalid Protocol")


def submit_update(request):
  """Submit Maintenance Window info to Cluster/Tenant Combo"""
  is_general_user(request)
  if request.method == "POST":
    if request.is_ajax():
      form = create_maintenance_window(request.POST)
      # print(request.POST)
      if form.is_valid():
        # Popping all the args to get strip the information to a valid formset

        post_data = request.POST.copy()
        post_data.pop['maintenance_window_id']
        cluster_name = request.POST['cluster_name']
        tenant_name = request.POST['tenant_name']
        payload = parse_submit_form(post_data)
        try:
          print(payload)
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
      print("not ajax")
      return HttpResponseBadRequest("Invalid Call!")
  return HttpResponseBadRequest("Invalid Protocol")

def get_window_details(request):
  """Extract Maintenance Window Information"""
  is_general_user(request)
  if request.method == "POST" and request.is_ajax():
    cluster = request.POST['cluster_name']
    tenant = request.POST['tenant_name']
    window_id = request.POST['window_id']

    window_details = maintenance.get_window(
        uv.FULL_SET[cluster], tenant, window_id)
    return JsonResponse(window_details)
  return HttpResponseBadRequest("Invalid!")


def get_all_windows(request):
  is_general_user(request)
  if request.method == 'POST' and request.is_ajax():
    # form = view_maintenance_window(request.POST)
    cluster = uv.FULL_SET[request.POST['cluster_name']]
    list_of_windows = maintenance.get_windows(
        cluster, request.POST['tenant_name'])
    return JsonResponse(list_of_windows)
  return HttpResponseBadRequest("Invalid!")
