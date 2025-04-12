# signmeet/ml_models/asl_detection/utils.py
import cv2
import numpy as np

def preprocess_frame(frame):
    # Convert BGR to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Resize to 224x224 (assuming model input size)
    frame_resized = cv2.resize(frame_rgb, (64, 64))
    # Normalize to [0, 1]
    frame_normalized = frame_resized.astype(np.float32) / 255.0
    return frame_normalized