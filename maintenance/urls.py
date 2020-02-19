from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create, name='create-window'),
    path('view/', views.view, name='view-window'),
    path('submit_create', views.submit_create, name='submit-create-window'),
    path('submit_view', views.submit_view, name='submit-view-window'),
]
