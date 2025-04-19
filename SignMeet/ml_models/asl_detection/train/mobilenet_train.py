import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from torch.utils.data import DataLoader, Subset
from torchvision.datasets import ImageFolder
import os
from sklearn.model_selection import train_test_split

def train_model():
    # Define augmented transforms to match inference
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(15),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    # Load dataset
    dataset_path = "C:\\DISHA\\sign\\archive (6)\\ASL_Alphabet_Dataset\\asl_alphabet_train"
    print(f"Loading dataset from: {dataset_path}")
    try:
        dataset = ImageFolder(dataset_path, transform=transform)
        print(f"Dataset loaded with {len(dataset)} samples and {len(dataset.classes)} classes")
        class_counts = {cls: len(os.listdir(os.path.join(dataset_path, cls))) for cls in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, cls))}
        print("Class distribution:", class_counts)
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return

    # Split dataset (80% train, 20% validation)
    train_idx, val_idx = train_test_split(list(range(len(dataset))), test_size=0.2, stratify=[dataset.targets[i] for i in range(len(dataset))])
    train_dataset = Subset(dataset, train_idx)
    val_dataset = Subset(dataset, val_idx)
    print(f"Training samples: {len(train_dataset)}, Validation samples: {len(val_dataset)}")

    # Use single worker to avoid Windows multiprocessing issues
    loader = DataLoader(train_dataset, batch_size=16, shuffle=True, num_workers=0, pin_memory=True)
    val_loader = DataLoader(val_dataset, batch_size=16, shuffle=False, num_workers=0, pin_memory=True)

    # Load pretrained MobileNetV2
    model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.IMAGENET1K_V1)
    num_classes = len(dataset.classes)
    print(f"Number of classes detected: {num_classes}")
    model.classifier[1] = nn.Linear(model.classifier[1].in_features, num_classes)
    model = model.to('cuda')

    # Unfreeze last 3 blocks for fine-tuning
    for param in model.features[-3:].parameters():
        param.requires_grad = True

    # Loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(filter(lambda p: p.requires_grad, model.parameters()), lr=0.0001)

    # Training loop
    num_epochs = 10
    best_val_loss = float('inf')
    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        for i, (inputs, labels) in enumerate(loader):
            print(f"Epoch {epoch+1}/{num_epochs}, Batch {i+1}/{len(loader)}, Processing...")
            inputs, labels = inputs.to('cuda', non_blocking=True), labels.to('cuda', non_blocking=True)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()

        # Validation
        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.to('cuda'), labels.to('cuda')
                outputs = model(inputs)
                val_loss += criterion(outputs, labels).item()
        val_loss /= len(val_loader)
        print(f"Epoch {epoch+1}/{num_epochs}, Train Loss: {running_loss/len(loader)}, Val Loss: {val_loss}")
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            torch.save(model.state_dict(), 'mobilenetv2_asl_trained_improved_best.pth')
            print("New best model saved")

    # Final save
    model_path = os.path.join("C:\\DISHA\\6th sem\\Minor Project\\SignMeet\\ml_models\\asl_detection", "mobilenetv2_asl_trained_improved.pth")
    torch.save(model.state_dict(), model_path)
    print(f"Model saved to {model_path}")

if __name__ == '__main__':
    train_model()