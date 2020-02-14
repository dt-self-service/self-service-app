from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create, name='create-window'),
    path('view/', views.view, name='view-window'),
]
