from django.urls import path
from . import views
from django.shortcuts import redirect


def redirect_to_home(request):
    return redirect('/')
urlpatterns = [
    path('', views.home, name='home'),
    path('video-call/<str:room_name>/', views.video_call, name='video_call'),
    path('get_token/', views.get_agora_token, name='get_agora_token'),
]
