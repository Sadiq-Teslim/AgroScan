import cv2
import numpy as np
import os
from PIL import Image

# Paths
split_dataset_path = r"c:\Users\hp\OneDrive\Desktop\Tech\Projects Folder\AgroScan\AgroScan-1\plant_data\split_dataset"

# Preprocessing function
def preprocess_image(image_path, output_path, img_size=(224, 224)):
    """
    Preprocess an image for model inference.
    - Resize to the required input size.
    - Normalize pixel values.
    - Apply noise reduction.
    """
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Failed to load image: {image_path}")
        return

    # Resize the image
    image_resized = cv2.resize(image, img_size)

    # Convert to RGB (if needed)
    image_rgb = cv2.cvtColor(image_resized, cv2.COLOR_BGR2RGB)

    # Apply noise reduction
    image_denoised = cv2.fastNlMeansDenoisingColored(image_rgb, None, 10, 10, 7, 21)

    # Normalize pixel values to [0, 1]
    image_normalized = image_denoised / 255.0

    # Save the preprocessed image
    output_file = os.path.join(output_path, os.path.basename(image_path))
    Image.fromarray((image_normalized * 255).astype(np.uint8)).save(output_file)
    print(f"Preprocessed image saved at: {output_file}")

# Process all images in the train, val, and test folders
for split in ["train", "val", "test"]:
    split_path = os.path.join(split_dataset_path, split)
    for class_folder in os.listdir(split_path):
        class_folder_path = os.path.join(split_path, class_folder)
        if os.path.isdir(class_folder_path):
            for image_file in os.listdir(class_folder_path):
                image_path = os.path.join(class_folder_path, image_file)
                if os.path.isfile(image_path):
                    preprocess_image(image_path, class_folder_path)

print("Image preprocessing completed!")