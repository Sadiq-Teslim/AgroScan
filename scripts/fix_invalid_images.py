from PIL import Image
import os

# Path to the dataset
dataset_path = r"c:\Users\hp\OneDrive\Desktop\Tech\Projects Folder\AgroScan\AgroScan-1\plant_data\split_dataset"

# Function to check if an image is valid
def is_valid_image(file_path):
    try:
        with Image.open(file_path) as img:
            img.verify()  # Verify that it is an image
        return True
    except Exception:
        return False

# Function to scan and fix invalid images
def fix_invalid_images(dataset_path):
    for split in ["train", "val", "test"]:
        split_path = os.path.join(dataset_path, split)
        for class_folder in os.listdir(split_path):
            class_folder_path = os.path.join(split_path, class_folder)
            if os.path.isdir(class_folder_path):
                for image_file in os.listdir(class_folder_path):
                    image_path = os.path.join(class_folder_path, image_file)
                    if not is_valid_image(image_path):
                        print(f"Invalid image file found: {image_path}")
                        # Uncomment the next line to delete invalid files
                        os.remove(image_path)
                        print(f"Deleted invalid image file: {image_path}")

# Run the script
fix_invalid_images(dataset_path)
print("Invalid image check completed!")