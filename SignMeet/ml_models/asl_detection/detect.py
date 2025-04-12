# signmeet/ml_models/asl_detection/detect.py
import os
import sys
import cv2
import numpy as np
import tensorflow as tf

# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Add project root to sys.path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '../../..'))  # Adjust to SignMeet root
sys.path.append(project_root)
from ml_models.asl_detection.utils import preprocess_frame

# Path to your trained model
MODEL_PATH = os.path.join(project_root, 'signmeet/ml_models/asl_detection/asl_model2.h5')
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print("Model loaded successfully from", MODEL_PATH)
except Exception as e:
    print(f"Failed to load model: {e}")
    model = None

# Classes for ASL digits and letters
ASL_CLASSES = ['1', '2', '3', '4', '5', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

def detect_signs(frame):
    if model is None:
        print("Model not loaded. Returning '[None]'")
        return "[None]"

    try:
        processed_frame = preprocess_frame(frame)
        processed_frame = np.expand_dims(processed_frame, axis=0)
        predictions = model.predict(processed_frame, verbose=0)
        predicted_class_idx = np.argmax(predictions[0])
        if 0 <= predicted_class_idx < len(ASL_CLASSES):
            translation = ASL_CLASSES[predicted_class_idx]
        else:
            translation = "[Unknown]"
        print(f"Predicted class index: {predicted_class_idx}, Translation: {translation}")
        return translation
    except Exception as e:
        print(f"Error during detection: {e}")
        return "[Error]"

def detect_signs_from_bytes(bytes_data):
    if model is None:
        return "[None]"
    
    try:
        # Convert bytes to NumPy array
        nparr = np.frombuffer(bytes_data, np.uint8)
        if len(nparr) == 0:
            print("Empty byte data received")
            return "[Error]"
        
        # Decode the image
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if frame is None:
            print(f"Failed to decode image. Byte data length: {len(bytes_data)}")
            return "[Error]"
        
        # Debug: Check frame shape
        print(f"Decoded frame shape: {frame.shape}")
        return detect_signs(frame)
    except Exception as e:
        print(f"Error during byte decoding: {e}")
        return "[Error]"

if __name__ == "__main__":
    test_image_path = os.path.join(project_root, 'signmeet/ml_models/asl_detection/test_image.jpg')
    test_frame = cv2.imread(test_image_path)
    if test_frame is not None:
        translation = detect_signs(test_frame)
        print(f"Test detection result: {translation}")