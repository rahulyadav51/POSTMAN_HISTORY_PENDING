from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_client, name='api_client'),
]