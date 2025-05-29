import torch
from torchvision import transforms, models
from PIL import Image

# Paths
model_path = r"c:\Users\hp\OneDrive\Desktop\Tech\Projects Folder\AgroScan\AgroScan-1\AI_models\mobilenetv2_finetuned.pth"

# Parameters
IMG_SIZE = 224
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Data transformations
transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Load the trained model
model = models.mobilenet_v2()
NUM_CLASSES = 9  # Update this based on your dataset
model.classifier[1] = torch.nn.Linear(model.last_channel, NUM_CLASSES)
model.load_state_dict(torch.load(model_path))
model = model.to(DEVICE)
model.eval()  # Set model to evaluation mode

# Class names (update this with your dataset's class names)
class_names = [
    'Pepper__bell___Bacterial_spot',
    'Pepper__bell___healthy',
    'Potato___Early_blight',
    'Potato___Late_blight',
    'Potato___healthy',
    'Tomato_Bacterial_spot',
    'Tomato_Early_blight',
    'Tomato_Late_blight',
    'Tomato_healthy'
]

# Function to predict the class of a single image
def predict_image(image_path):
    try:
        # Load and preprocess the image
        image = Image.open(image_path).convert('RGB')
        image = transform(image).unsqueeze(0).to(DEVICE)

        # Perform inference
        with torch.no_grad():
            outputs = model(image)
            _, predicted = torch.max(outputs, 1)
            class_name = class_names[predicted.item()]
            print(f"Predicted Disease: {class_name}")
    except Exception as e:
        print(f"Error processing image: {e}")

# Interactive loop for testing images
print("Enter the path to an image to test it. Enter '-1' to stop.")
while True:
    image_path = input("Image Path: ")
    if image_path == '-1':
        print("Exiting...")
        break
    predict_image(image_path)