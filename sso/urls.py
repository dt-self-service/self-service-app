from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='saml-index'),
    path('attrs/', views.attrs, name='saml-attrs'),
    path('metadata/', views.metadata, name='saml-metadata'),
]
