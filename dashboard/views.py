from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

import user_variables as uv

# Create your views here.
def home(request):
    return render(request, 'dashboard/index.html')

def tables(request):
    return render(request, 'dashboard/tables.html')

def get_tenant(request):
    if request.method == "GET":
        cluster = request.GET['chosen_cluster'] #TODO Request Validation
        if cluster == "":
            return JsonResponse({})
        i = 0
        tenant_json = {}
        for tenant in uv.FULL_SET[cluster]["tenant"]:
            i = i + 1
            tenant_json[i] = tenant
        return JsonResponse(tenant_json)