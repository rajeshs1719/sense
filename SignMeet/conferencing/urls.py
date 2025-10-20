from django.urls import path
from . import views

urlpatterns = [
    # Your existing paths
    path('', views.home, name='home'),
    path('room/<str:room_name>/', views.video_call, name='video_call'),
    path('get_token/', views.get_agora_token, name='get_agora_token'),

    # --- Add this new path for the chatbot ---
    path('chat/send_message/', views.sense_chat_message, name='sense_chat_message'),
    path('api/dynamic_tts/', views.generate_dynamic_tts, name='api_dynamic_tts'),
]