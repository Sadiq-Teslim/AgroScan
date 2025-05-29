import torch
import torch.nn as nn
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
import os

# Paths to the dataset
#train_dir = r"c:\Users\hp\OneDrive\Desktop\Tech\Projects Folder\AgroScan\AgroScan-1\plant_data\split_dataset\train"
val_dir = r"c:\Users\hp\OneDrive\Desktop\Tech\Projects Folder\AgroScan\AgroScan-1\plant_data\split_dataset\val"

# Check if directories exist and are not empty
#if not os.path.exists(train_dir) or not os.listdir(train_dir):
#    raise FileNotFoundError(f"Train directory is empty or does not exist: {train_dir}")

if not os.path.exists(val_dir) or not os.listdir(val_dir):
    raise FileNotFoundError(f"Validation directory is empty or does not exist: {val_dir}")

# Debug directory contents
#print("Train directory contents:", os.listdir(train_dir))
print("Validation directory contents:", os.listdir(val_dir))

# Custom function to validate file extensions
def is_valid_file(file_path):
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp', '.JPG', '.JPEG', '.PNG', '.BMP', '.TIFF', '.WEBP')
    return file_path.lower().endswith(valid_extensions)

# Filter out invalid directories (e.g., split_dataset)
def filter_valid_class_folders(directory):
    return [folder for folder in os.listdir(directory) if os.path.isdir(os.path.join(directory, folder))]

# Filtered class folders
#train_classes = filter_valid_class_folders(train_dir)
val_classes = filter_valid_class_folders(val_dir)

#print("Filtered train classes:", train_classes)
print("Filtered validation classes:", val_classes)

# Parameters
IMG_SIZE = 224
BATCH_SIZE = 16
NUM_CLASSES = len(val_classes)  # Number of categories
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Data transformations
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Datasets and DataLoaders
#train_dataset = datasets.ImageFolder(train_dir, transform=transform, is_valid_file=is_valid_file)
val_dataset = datasets.ImageFolder(val_dir, transform=transform, is_valid_file=is_valid_file)

print("Validation dataset loaded successfully!")

#train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=True)

# Load pre-trained MobileNetV2
model = models.mobilenet_v2()  # Initialize MobileNetV2 without weights

# Path to the manually downloaded weights file
weights_path = r"c:\Users\hp\Downloads\mobilenet_v2-b0353104.pth"

# Load the weights into the model
model.load_state_dict(torch.load(weights_path))

# Modify the classifier for the number of classes in your dataset
model.classifier[1] = nn.Linear(model.last_channel, NUM_CLASSES)

# Move model to device
model = model.to(DEVICE)

# Load the fine-tuned model weights
model.load_state_dict(torch.load(r"c:\Users\hp\OneDrive\Desktop\Tech\Projects Folder\AgroScan\AgroScan-1\AI_models\mobilenetv2_finetuned.pth"))
model.train()  # Ensure the model is in training mode

# Loss function and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Training loop
EPOCHS = 5  # Increase the number of epochs
for epoch in range(EPOCHS):
    model.train()
    running_loss = 0.0
    for batch_idx, (inputs, labels) in enumerate(val_loader, start=1):  # Add batch index
        inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)

        # Print the batch index
        print(f"Training Batch {batch_idx}/{len(val_loader)}")

        # Print the disease folder (class) and image being trained on
        for i in range(len(inputs)):
            class_name = val_dataset.classes[labels[i].item()]
            print(f"Training on class: {class_name}, Image index: {i}")

        # Forward pass
        outputs = model(inputs)
        loss = criterion(outputs, labels)

        # Backward pass and optimization
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        running_loss += loss.item()

    print(f"Epoch {epoch+1}/{EPOCHS}, Loss: {running_loss/len(val_loader):.4f}")

# Save the trained model
    torch.save(model.state_dict(), r"c:\Users\hp\OneDrive\Desktop\Tech\Projects Folder\AgroScan\AgroScan-1\AI_models\mobilenetv2_finetuned.pth")

print("Model training completed and saved!")
