from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='admin-home'),
    path('tables/', views.tables, name='tables'),
    path('get_tenant', views.get_tenant),
]