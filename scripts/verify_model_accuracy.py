import tensorflow as tf
import numpy as np
from PIL import Image
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import os

# Load the TFLite model
def load_model(model_path):
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    print("Model loaded successfully!")
    print("Input details:", input_details)
    print("Output details:", output_details)
    return interpreter, input_details, output_details

# Preprocess images for validation
def preprocess_image(image_path, input_shape):
    """
    Preprocess the image to match the model's input shape.
    Converts the image to channels-first format [batch_size, channels, height, width].
    """
    image = Image.open(image_path).convert("RGB")
    image = image.resize((input_shape[2], input_shape[3]))# Resize to [height, width]
    image = np.array(image, dtype=np.float32) / 255.0  # Normalize to [0, 1]
    image = np.transpose(image, (2, 0, 1))  # Convert to channels-first format [channels, height, width]
    image = np.expand_dims(image, axis=0)  # Add batch dimension [1, channels, height, width]
    return image

# Run inference on a single image
def run_inference(interpreter, input_details, output_details, image_path):
    input_shape = input_details[0]['shape']
    input_data = preprocess_image(image_path, input_shape)

    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    output_data = interpreter.get_tensor(output_details[0]['index'])
    return np.argmax(output_data), output_data  # Predicted class and confidence scores

# Evaluate model performance
def evaluate_model(interpreter, input_details, output_details, validation_dataset):
    true_labels = []  # Ground truth labels
    predicted_labels = []  # Model predictions

    for image_path, label in validation_dataset:
        predicted_class, _ = run_inference(interpreter, input_details, output_details, image_path)
        true_labels.append(label)
        predicted_labels.append(predicted_class)

    # Calculate metrics
    accuracy = accuracy_score(true_labels, predicted_labels)
    precision = precision_score(true_labels, predicted_labels, average="weighted")
    recall = recall_score(true_labels, predicted_labels, average="weighted")
    f1 = f1_score(true_labels, predicted_labels, average="weighted")

    print(f"Accuracy: {accuracy:.2f}")
    print(f"Precision: {precision:.2f}")
    print(f"Recall: {recall:.2f}")
    print(f"F1-Score: {f1:.2f}")

    return accuracy, precision, recall, f1

# Path to the TFLite model
model_path = "AI_models\mobilenetv2_finetuned_quantized.tflite"

# Path to the validation dataset
validation_dir = r"plant_data\val_subset"  # Use raw string to avoid escape sequences
class_mapping = {
    "Pepper_b_b_s": 0,
    "Pepper_b_h": 1,
    # "Potato_Early_blight": 2,
    # "Potato_Late_blight": 3,
    # "Potato_healthy": 4,
    # "Tomato_Bacterial_spot": 5,
    # "Tomato_Early_blight": 6,
    # "Tomato_Late_blight": 7,
    #"Tomato_healthy": 0,
    # Add more classes as needed
}

# Load validation dataset
def load_validation_dataset(validation_dir, class_mapping):
    dataset = []
    for class_name, label in class_mapping.items():
        class_dir = os.path.join(validation_dir, class_name)
        print(f"Processing directory: {class_dir}")  # Debugging
        if not os.path.exists(class_dir):
            print(f"Directory does not exist: {class_dir}")
            continue
        for image_name in os.listdir(class_dir):
            image_path = os.path.join(class_dir, image_name)
            dataset.append((image_path, label))
    return dataset

# Main function
if __name__ == "__main__":
    # Load the model
    interpreter, input_details, output_details = load_model(model_path)

    # Load the validation dataset
    validation_dataset = load_validation_dataset(validation_dir, class_mapping)

    # Evaluate the model
    evaluate_model(interpreter, input_details, output_details, validation_dataset)