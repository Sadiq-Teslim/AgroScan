
## 2. Document the AI Model

Create an `AI_MODEL.md` file:
```markdown
# AgroScan AI Model

## Model Architecture
- Base: MobileNetV2
- Input Shape: 224x224x3
- Output Classes: 9 (various plant diseases)

## Classes
1. Pepper_bell_Bacterial_spot
2. Pepper_bell_healthy
3. Potato_Early_blight
4. Potato_Late_blight
5. Potato_healthy
6. Tomato_Bacterial_spot
7. Tomato_Early_blight
8. Tomato_Late_blight
9. Tomato_healthy

## Model Files
- mobilenetv2_finetuned_quantized.tflite: Optimized TFLite model
- mobilenetv2_finetuned_tf/: SavedModel directory

## Preprocessing
Images are resized to 224x224 and normalized to [0,1].