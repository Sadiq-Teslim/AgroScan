import os

# Path to the dataset
dataset_path = r"C:\Users\hp\OneDrive\Desktop\Tech\Projects Folder\AgroScan\AgroScan-1\plant_data\plantVillage"

# Analyze the dataset
print("Analyzing dataset...")
for category in os.listdir(dataset_path):
    category_path = os.path.join(dataset_path, category)
    if os.path.isdir(category_path):  # Ensure it's a directory
        num_images = len([img for img in os.listdir(category_path) if os.path.isfile(os.path.join(category_path, img))])
        print(f"{category}: {num_images} images")