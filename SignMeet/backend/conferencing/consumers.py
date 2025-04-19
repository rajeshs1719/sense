# SignMeet/conferencing/consumers.py
import sys
import os
from channels.generic.websocket import AsyncWebsocketConsumer

# Add the signmeet directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from ml_models.asl_detection.wlasl_detection import detect_signs_from_bytes

class SignDetectionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print("WebSocket connected for sign detection")

    async def disconnect(self, close_code):
        print("WebSocket disconnected")

    async def receive(self, text_data=None, bytes_data=None):
        if bytes_data:
            try:
                print(f"Received bytes data length: {len(bytes_data)}")
                translation = detect_signs_from_bytes(bytes_data)
                await self.send(text_data=translation)
                print(f"Predicted sign: {translation}")
            except Exception as e:
                print(f"Error in SignDetectionConsumer: {e}")
                await self.send(text_data="[Error]")