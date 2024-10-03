import os
import tensorflow as tf
import numpy as np
import cv2
import tensorflow_hub as hub

# Load compressed models from tensorflow_hub
os.environ['TFHUB_MODEL_LOAD_FORMAT'] = 'COMPRESSED'

# Load style transfer model from TensorFlow Hub
hub_model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')

# Function to process a video frame and apply neural style transfer
def process_frame(frame, style_image):
    # Convert frame from BGR (OpenCV format) to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Convert the frame to a TensorFlow tensor and add a batch dimension
    frame_rgb = tf.convert_to_tensor(frame_rgb, dtype=tf.float32)
    frame_rgb = frame_rgb[tf.newaxis, :]
    
    # Apply the style transfer model
    stylized_frame = hub_model(tf.constant(frame_rgb), tf.constant(style_image))[0]
    
    # Convert the output tensor to a NumPy array and back to BGR for OpenCV
    stylized_frame = tensor_to_image(stylized_frame)
    
    return stylized_frame

# Function to convert TensorFlow tensor to image
def tensor_to_image(tensor):
    tensor = tensor * 255
    tensor = np.array(tensor, dtype=np.uint8)
    if np.ndim(tensor) > 3:
        assert tensor.shape[0] == 1
        tensor = tensor[0]
    
    # Convert to BGR format for OpenCV
    if tensor.shape[-1] == 3:  # RGB image
        tensor = cv2.cvtColor(tensor, cv2.COLOR_RGB2BGR)
    
    return tensor

# Load and preprocess style image
def load_img(path_to_img):
    max_dim = 512
    img = tf.io.read_file(path_to_img)
    img = tf.image.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)

    shape = tf.cast(tf.shape(img)[:-1], tf.float32)
    long_dim = max(shape)
    scale = max_dim / long_dim

    new_shape = tf.cast(shape * scale, tf.int32)
    img = tf.image.resize(img, new_shape)
    img = img[tf.newaxis, :]  # Add batch dimension
    return img

# Paths to content video and style image
video_path = 'content.mp4'
style_path = 'Data/Wallpaper_1.jpeg'

# Load and preprocess the style image
style_image = load_img(style_path)

# Capture the video using OpenCV
cap = cv2.VideoCapture(video_path)

# Get video properties
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define video writer to save the output video
output_path = 'styled_video.avi'
out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'XVID'), fps, (width, height))

# Process video frame by frame
frame_count = 0
while cap.isOpened():
    ret, frame = cap.read()
    
    if not ret:
        break
    
    # Apply style transfer to the current frame
    stylized_frame = process_frame(frame, style_image)
    
    # Write the processed frame to the output video
    out.write(stylized_frame)
    
    frame_count += 1
    print(f'Processed frame {frame_count}', end='\r')

# Release video capture and writer
cap.release()
out.release()
cv2.destroyAllWindows()

print("Video processing completed.")
