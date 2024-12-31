from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_event_view, name='create_event'),
    path('events/', views.event_list_view, name='event_list'),
    # path('myevents/', views.my_events, name='my_events'),
    path('events/<int:id>/', views.event_detail, name='event_detail'),
]
