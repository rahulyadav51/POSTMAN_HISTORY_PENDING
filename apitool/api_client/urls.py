# from django.urls import path
# from . import views

# urlpatterns = [
#     # path('', views.send_api_request, name='api_client'),
#     path('', views.api_client, name='api_client'),

# ]

from django.urls import path
from . import views

# urlpatterns = [
#     path('api-client/', views.api_client, name='api_client'),
#     path('history/<int:history_id>/', views.get_history_detail, name='get_history_detail'),
# ]
urlpatterns = [
    path('api-client/', views.api_client, name='api_client'),
    path('history/<int:history_id>/', views.get_history_detail, name='get_history_detail'),
    path('get-history/', views.get_history, name='get-history'),

]