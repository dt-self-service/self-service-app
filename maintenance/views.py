from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import create_maintenance_window
# Create your views here.
def create(request):
    if request.method == "POST":

        form = create_maintenance_window(request.POST)
        if form.is_valid():
            pass
    else:
        form = create_maintenance_window()
    return render(request, 'maintenance/create.html', {'form': form})