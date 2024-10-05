import tensorflow_hub as hub

# Path to the extracted model directory
model_dir = "Model"

# Load the model from the local directory
hub_model = hub.load(model_dir)

print("Model loaded successfully from the local directory!")
