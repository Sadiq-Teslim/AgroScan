import tensorflowjs as tfjs
import os

# Paths
saved_model_path = r"C:\Users\hp\OneDrive\Desktop\Tech\Projects Folder\AgroScan\AgroScan-1\AI_models\mobilenetv2_finetuned_tf"
tfjs_output_path = r"c:\Users\hp\OneDrive\Desktop\Tech\Projects Folder\AgroScan\AgroScan-1\frontend\tfjs_model"

# Ensure the output directory exists
os.makedirs(tfjs_output_path, exist_ok=True)

# Convert the SavedModel to TensorFlow.js format
print("Converting SavedModel to TensorFlow.js format...")
tfjs.converters.convert_tf_saved_model(saved_model_path, tfjs_output_path)

print(f"TensorFlow.js model saved at: {tfjs_output_path}")