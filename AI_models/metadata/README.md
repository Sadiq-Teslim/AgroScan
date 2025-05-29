# MobileNetV2 Fine-Tuned Model

This directory contains the fine-tuned MobileNetV2 model for crop disease detection.

## Files
- `mobilenetv2_finetuned_quantized.tflite`: Optimized TensorFlow Lite model for deployment.
- `mobilenetv2_finetuned.onnx`: ONNX model for interoperability (optional).
- `mobilenetv2_finetuned.pth`: PyTorch model for retraining or further fine-tuning.
- `metadata/model_info.json`: Metadata about the model.
- `metadata/class_mapping.json`: Mapping of class names to labels.

## Usage
- Input shape: `[1, 3, 224, 224]`
- Output shape: `[1, 9]`
- Preprocessing:
  - Resize images to `[224, 224]`.
  - Normalize pixel values to `[0, 1]`.
  - Convert to channels-first format.