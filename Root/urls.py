from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("head/", include('Head.urls')),
    path('account/', include('Account.urls')),
    path('event/', include('Event.urls')),
    path('calendar/', include('Calendar.urls')),
]
