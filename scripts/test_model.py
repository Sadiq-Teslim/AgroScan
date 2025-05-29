import torch
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader

# Paths
test_dir = r"c:\Users\hp\OneDrive\Desktop\Tech\Projects Folder\AgroScan\AgroScan-1\plant_data\split_dataset\test"
model_path = r"c:\Users\hp\OneDrive\Desktop\Tech\Projects Folder\AgroScan\AgroScan-1\AI_models\mobilenetv2_finetuned.pth"

# Parameters
IMG_SIZE = 224
BATCH_SIZE = 16
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Data transformations
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Load validation dataset
test_dataset = datasets.ImageFolder(test_dir, transform=transform)
test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)

# Load the trained model
model = models.mobilenet_v2()
NUM_CLASSES = len(test_dataset.classes)
model.classifier[1] = torch.nn.Linear(model.last_channel, NUM_CLASSES)
model.load_state_dict(torch.load(model_path))
model = model.to(DEVICE)
model.eval()  # Set model to evaluation mode

# Evaluate the model
correct = 0
total = 0 
with torch.no_grad():
    for inputs, labels in test_loader:
        inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)
        outputs = model(inputs)
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

accuracy = 100 * correct / total
print(f"Testing Accuracy: {accuracy:.2f}%")