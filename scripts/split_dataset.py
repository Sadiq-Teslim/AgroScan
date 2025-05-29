import os
import shutil
from sklearn.model_selection import train_test_split

dataset_path = r"c:\Users\hp\OneDrive\Desktop\Tech\Projects Folder\AgroScan\AgroScan-1\plant_data\plantVillage"
output_path = r"c:\Users\hp\OneDrive\Desktop\Tech\Projects Folder\AgroScan\AgroScan-1\plant_data\split_dataset"

# Create output directories
for split in ['train', 'val', 'test']:
    split_path = os.path.join(output_path, split)
    os.makedirs(split_path, exist_ok=True)

# Split each class
for class_folder in os.listdir(dataset_path):
    class_path = os.path.join(dataset_path, class_folder)
    if os.path.isdir(class_path):
        images = os.listdir(class_path)

        # Handle small categories
        if len(images) < 3:
            print(f"Skipping splitting for {class_folder} (only {len(images)} images)")
            split_class_path = os.path.join(output_path, 'train', class_folder)
            os.makedirs(split_class_path, exist_ok=True)
            for img in images:
                src = os.path.join(class_path, img)
                dest = os.path.join(split_class_path, img)
                if os.path.isfile(src):  # Ensure it's a file
                    shutil.copy(src, dest)
            continue

        # Ensure there are enough images to split
        if len(images) < 10:
            print(f"Not enough images to split {class_folder} into train, val, and test. Assigning all to train.")
            split_class_path = os.path.join(output_path, 'train', class_folder)
            os.makedirs(split_class_path, exist_ok=True)
            for img in images:
                src = os.path.join(class_path, img)
                dest = os.path.join(split_class_path, img)
                if os.path.isfile(src):  # Ensure it's a file
                    shutil.copy(src, dest)
            continue

        # Split into train, val, and test
        train, temp = train_test_split(images, test_size=0.3, random_state=42)

        # Check if temp has enough samples for further splitting
        if len(temp) < 2:
            print(f"Not enough images to split {class_folder} into val and test. Assigning all to train.")
            split_class_path = os.path.join(output_path, 'train', class_folder)
            os.makedirs(split_class_path, exist_ok=True)
            for img in images:
                src = os.path.join(class_path, img)
                dest = os.path.join(split_class_path, img)
                if os.path.isfile(src):  # Ensure it's a file
                    shutil.copy(src, dest)
            continue

        val, test = train_test_split(temp, test_size=0.5, random_state=42)  # Split temp into 50% val, 50% test

        # Copy images to respective folders
        for split, split_images in zip(['train', 'val', 'test'], [train, val, test]):
            split_class_path = os.path.join(output_path, split, class_folder)
            os.makedirs(split_class_path, exist_ok=True)
            for img in split_images:
                src = os.path.join(class_path, img)
                dest = os.path.join(split_class_path, img)
                if os.path.isfile(src):  # Ensure it's a file
                    shutil.copy(src, dest)

print("Dataset split completed!")