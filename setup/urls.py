from django.urls import path
from . import views

urlpatterns = [
    path('initial/', views.initial, name='initial'),
    path('smtp/', views.smtp, name='smtp'),
    path('finish/', views.finish, name='finish'),
]