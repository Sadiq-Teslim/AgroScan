import torch
import onnx
import tensorflow as tf
import os

# Paths
trained_model_path = r"c:\Users\hp\OneDrive\Desktop\Tech\Projects Folder\AgroScan\AgroScan-1\AI_models\mobilenetv2_finetuned.pth"
onnx_model_path = r"c:\Users\hp\OneDrive\Desktop\Tech\Projects Folder\AgroScan\AgroScan-1\AI_models\mobilenetv2_finetuned.onnx"
tf_model_path = r"c:\Users\hp\OneDrive\Desktop\Tech\Projects Folder\AgroScan\AgroScan-1\AI_models\mobilenetv2_finetuned_tf"
tflite_model_path = r"c:\Users\hp\OneDrive\Desktop\Tech\Projects Folder\AgroScan\AgroScan-1\AI_models\mobilenetv2_finetuned.tflite"
quantized_tflite_model_path = r"c:\Users\hp\OneDrive\Desktop\Tech\Projects Folder\AgroScan\AgroScan-1\AI_models\mobilenetv2_finetuned_quantized.tflite"

# Step 1: Load the trained PyTorch model
print("Loading trained PyTorch model...")
from torchvision import models
model = models.mobilenet_v2()

# Modify the classifier to match the fine-tuned model
num_classes = 9  # Number of classes in your fine-tuned model
model.classifier[1] = torch.nn.Linear(model.last_channel, num_classes)

# Load the fine-tuned weights
model.load_state_dict(torch.load(trained_model_path))
model.eval()

# Step 2: Convert PyTorch model to ONNX
print("Converting PyTorch model to ONNX format...")
dummy_input = torch.randn(1, 3, 224, 224)  # Example input size
torch.onnx.export(
    model,
    dummy_input,
    onnx_model_path,
    export_params=True,
    opset_version=11,
    do_constant_folding=True,
    input_names=['input'],
    output_names=['output']
)
print(f"ONNX model saved at: {onnx_model_path}")

# Step 3: Convert ONNX model to TensorFlow
print("Converting ONNX model to TensorFlow format...")
from onnx_tf.backend import prepare
onnx_model = onnx.load(onnx_model_path)
tf_rep = prepare(onnx_model)
tf_rep.export_graph(tf_model_path)
print(f"TensorFlow model saved at: {tf_model_path}")

# Step 4: Convert TensorFlow model to TFLite
print("Converting TensorFlow model to TensorFlow Lite format...")
converter = tf.lite.TFLiteConverter.from_saved_model(tf_model_path)
tflite_model = converter.convert()
with open(tflite_model_path, "wb") as f:
    f.write(tflite_model)
print(f"TFLite model saved at: {tflite_model_path}")

# Step 5: Apply quantization to the TFLite model
print("Applying quantization to the TFLite model...")
converter.optimizations = [tf.lite.Optimize.DEFAULT]
quantized_tflite_model = converter.convert()
with open(quantized_tflite_model_path, "wb") as f:
    f.write(quantized_tflite_model)
print(f"Quantized TFLite model saved at: {quantized_tflite_model_path}")

print("Model optimization completed!")