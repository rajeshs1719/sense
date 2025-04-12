# backend/routing.py
from django.urls import re_path
from . import consumers

print("Loading routing.py, consumers:", consumers)

websocket_urlpatterns = [
    re_path('/sign_detection', consumers.SignDetectionConsumer.as_asgi()),
]