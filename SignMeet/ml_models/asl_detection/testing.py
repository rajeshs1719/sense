import os
import glob
import time
import torch
import numpy as np
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report
import time
from torchvision import transforms, datasets
from tqdm import tqdm
from wlasl_detection import model

# Configuration
TEST_DATA_DIR = "C:/DISHA/sign/datasets/asl_alphabet_test"  # Folder with test images (subfolders by class)
BATCH_SIZE = 32
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
CLASS_NAMES = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
               'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 
               ]

# Load your trained model
model = model.to(DEVICE)
model.eval()

# Preprocessing
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Load test dataset
test_dataset = datasets.ImageFolder(TEST_DATA_DIR, transform=transform)
test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)

print(f"Testing on {len(test_dataset)} images across {len(CLASS_NAMES)} classes")

# Evaluation
all_preds = []
all_labels = []
inference_times = []

with torch.no_grad():
    for images, labels in tqdm(test_loader, desc="Testing"):
        images = images.to(DEVICE)
        labels = labels.to(DEVICE)
        
        # Measure inference time
        start_time = time.time()
        outputs = model(images)
        inference_times.append(time.time() - start_time)
        
        _, preds = torch.max(outputs, 1)
        
        all_preds.extend(preds.cpu().numpy())
        all_labels.extend(labels.cpu().numpy())

# Calculate metrics
accuracy = np.mean(np.array(all_preds) == np.array(all_labels))
avg_inference_time = np.mean(inference_times) * 1000  # Convert to ms
fps = 1000 / avg_inference_time

print(f"\nOverall Accuracy: {accuracy:.4f}")
print(f"Average Inference Time: {avg_inference_time:.2f}ms ({fps:.2f} FPS)")

# Classification Report
print("\nClassification Report:")
print(classification_report(all_labels, all_preds, target_names=CLASS_NAMES))

# Confusion Matrix
cm = confusion_matrix(all_labels, all_preds)
plt.figure(figsize=(15, 12))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", 
            xticklabels=CLASS_NAMES, yticklabels=CLASS_NAMES)
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.savefig("confusion_matrix.png", bbox_inches='tight')
plt.close()

# Class-wise Accuracy
class_correct = np.zeros(len(CLASS_NAMES))
class_total = np.zeros(len(CLASS_NAMES))

for i in range(len(CLASS_NAMES)):
    class_correct[i] = cm[i, i]
    class_total[i] = np.sum(cm[i, :])

class_accuracy = class_correct / class_total

plt.figure(figsize=(15, 6))
plt.bar(CLASS_NAMES, class_accuracy)
plt.xticks(rotation=45)
plt.ylabel("Accuracy")
plt.title("Class-wise Accuracy")
plt.savefig("class_accuracy.png", bbox_inches='tight')
plt.close()

# Inference Time Distribution
plt.figure(figsize=(10, 5))
plt.hist(np.array(inference_times) * 1000, bins=30)
plt.xlabel("Inference Time (ms)")
plt.ylabel("Frequency")
plt.title("Inference Time Distribution")
plt.savefig("inference_times.png", bbox_inches='tight')

print("\nVisualizations saved:")
print("- confusion_matrix.png")
print("- class_accuracy.png")
print("- inference_times.png")
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
from wlasl_detection import model  # Import your model and classes
from torchvision import transforms  # Add this line
import pandas as pd  # For easier data manipulation

ASL_CLASSES = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                ]
# --- Configuration ---
TEST_DATA_DIR = "C:/DISHA/sign/archive (6)/ASL_Alphabet_Dataset/asl_alphabet_test"  # Update this path
BATCH_SIZE = 32
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# --- Preprocessing ---
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# --- Custom Dataset Loader ---
class_names = ASL_CLASSES  # From your model definition
all_images = []
all_labels = []

# Map filenames to classes (e.g., "A_test.jpg" -> class 0)
for img_path in glob.glob(os.path.join(TEST_DATA_DIR, "*_test.jpg")):
    class_name = os.path.basename(img_path).split("_")[0].upper()
    if class_name in class_names:
        label = class_names.index(class_name)
        all_images.append(img_path)
        all_labels.append(label)

print(f"Found {len(all_images)} test images")

# --- Evaluation Mode ---
model = model.to(DEVICE)
model.eval()

# --- Metrics Tracking ---
all_preds = []
inference_times = []

# --- Testing Loop ---
with torch.no_grad():
    for img_path, true_label in zip(all_images, all_labels):
        img = Image.open(img_path).convert("RGB")
        img_tensor = transform(img).unsqueeze(0).to(DEVICE)  # Add batch dimension

        # Measure inference
        start_time = time.time()
        output = model(img_tensor)
        inference_times.append(time.time() - start_time)

        pred = torch.argmax(output).item()
        all_preds.append(pred)

# --- Calculate Metrics ---
accuracy = np.mean(np.array(all_preds) == np.array(all_labels))
avg_inference_time = np.mean(inference_times) * 1000  # ms

print(f"\nOverall Accuracy: {accuracy:.4f}")
print(f"Avg Inference Time: {avg_inference_time:.2f}ms")
print(f"FPS: {1 / (avg_inference_time / 1000):.2f}")

# --- Classification Report ---
print("\nClassification Report:")
report = classification_report(all_labels, all_preds, target_names=class_names)
print(report)

# --- Confusion Matrix ---
cm = confusion_matrix(all_labels, all_preds)
plt.figure(figsize=(12, 10))
sns.heatmap(cm, annot=True, fmt="d", xticklabels=class_names, yticklabels=class_names)
plt.title('Confusion Matrix')
plt.savefig("confusion_matrix.png")
plt.show()

# --- Alphabet-wise Accuracy Bar Chart ---
class_correct = [0] * len(class_names)
class_total = [0] * len(class_names)

for i in range(len(all_labels)):
    true_label = all_labels[i]
    predicted_label = all_preds[i]
    class_total[true_label] += 1
    if predicted_label == true_label:
        class_correct[true_label] += 1

class_accuracy = [class_correct[i] / class_total[i] if class_total[i] > 0 else 0 for i in range(len(class_names))]

plt.figure(figsize=(16, 8))
plt.bar(class_names, class_accuracy, color='skyblue')
plt.xlabel('ASL Alphabet')
plt.ylabel('Accuracy')
plt.title('Alphabet-wise Accuracy')
plt.ylim([0, 1])  # Set y-axis limit from 0 to 1
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig("alphabet_wise_accuracy.png")
plt.show()