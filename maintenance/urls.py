from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create, name='create-window'),
    path('view/', views.view, name='view-window'),
    path('update/', views.update, name='update-window'),
    path('delete/', views.delete, name='delete-window'),
    path('submit_create', views.submit_create, name='submit-create-window'),
    path('get_all_windows', views.get_all_windows, name='submit-get-all-windows'),
    path('get_window_details', views.get_window_details, name='submit-get-window-details'),
]
