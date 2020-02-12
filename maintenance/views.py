from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import create_maintenance_window
from packages.config import maintenance
import user_variables as uv

# Create your views here.
def create(request):
    if request.method == "POST":

        form = create_maintenance_window(request.POST)
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
            maintenance.create_window(
                    uv.FULL_SET[request.POST['cluster_name']],
                    request.POST['tenant_name'],
                    payload
            )
            print (payload)
    else:
        form = create_maintenance_window()
    return render(request, 'maintenance/create.html', {'form': form})

def day_options(request):
    pass
    