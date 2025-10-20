# SignMeet/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('conferencing.urls')),
    path('video-call/<str:room_name>/', include('conferencing.urls')),
]
