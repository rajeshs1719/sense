import os
import sys
import torch
import torch.nn as nn
import torchvision.models as models
import numpy as np
import cv2

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)

# Load MobileNetV2
model = models.mobilenet_v2(pretrained=False)
num_classes = 29
model.classifier[1] = nn.Linear(model.classifier[1].in_features, num_classes)
model.eval()

MODEL_PATH = os.path.join(script_dir, 'mobilenetv2_asl_trained_improved.pth')
if os.path.exists(MODEL_PATH):
    model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cpu')))
    print(f"MobileNetV2 ASL model loaded from {MODEL_PATH}")
else:
    raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")

# ASL Alphabet classes
ASL_CLASSES = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
               'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 
               'nothing', 'space']

def preprocess_frame(frame):
    print(f"Input frame shape: {frame.shape}")
    # Match dataset resolution and preprocessing
    frame_resized = cv2.resize(frame, (224, 224), interpolation=cv2.INTER_AREA)
    print(f"Resized frame shape: {frame_resized.shape}")
    # Exact normalization as training (ImageNet stats)
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    frame_normalized = (frame_resized.astype(np.float32) / 255.0 - mean) / std
    print(f"Normalized frame shape: {frame_normalized.shape}")
    frame_tensor = torch.from_numpy(frame_normalized).permute(2, 0, 1).unsqueeze(0).to(torch.float32)
    print(f"Tensor shape before return: {frame_tensor.shape}")
    return frame_tensor

def detect_sign(frame):
    try:
        with torch.no_grad():
            input_tensor = preprocess_frame(frame)
            print(f"Input tensor shape to model: {input_tensor.shape}")
            output = model(input_tensor)
            probabilities = torch.softmax(output, dim=1)
            predicted_class_idx = torch.argmax(output, dim=1).item()
            confidence = probabilities[0, predicted_class_idx].item()
            translation = ASL_CLASSES[predicted_class_idx] if confidence > 0.6 else "Uncertain"
            print(f"Predicted class index: {predicted_class_idx}, Translation: {translation}, Confidence: {confidence:.2f}, Output shape: {output.shape}")
            return translation
    except Exception as e:
        print(f"Error during detection: {e}")
        return "[Error]"

def detect_signs_from_bytes(bytes_data):
    try:
        nparr = np.frombuffer(bytes_data, np.uint8)
        print(f"Decoded array shape: {nparr.shape if nparr.shape else 'None (flat array)'}, Total bytes: {len(nparr)}")
        expected_bytes = 229 * 229 * 3
        if len(nparr) != expected_bytes:
            print(f"Invalid data length: {len(nparr)}, expected {expected_bytes}")
            return "[Error]"

        frame = nparr.reshape(229, 229, 3)
        print(f"Reshaped frame shape: {frame.shape}")
        return detect_sign(frame)
    except Exception as e:
        print(f"Error during byte processing: {e}")
        return "[Error]"

if __name__ == "__main__":
    test_image_path = os.path.join(os.path.dirname(__file__), 'test_image.jpg')
    test_frame = cv2.imread(test_image_path)
    if test_frame is not None:
        translation = detect_sign(test_frame)
        print(f"Test detection result: {translation}")