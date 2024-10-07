import tensorflow as tf
import tensorflow_hub as hub
import matplotlib.pyplot as plt
import numpy as np
import cv2
import PIL
import os

hub_model = hub.load('NST_Model')
print("Model loaded successfully from the local directory!")

class Video_Processing:

  def __init__(self, art_img_path, video_path):

    print("DEBUG: INSIDE INIT")
    self.art_img_path = art_img_path
    self.video_path = video_path
    self.style_im = None

  #read image, convert to tensor, normalize and resize 
  def image_read(self, image):
    max_dim=512
    image= tf.convert_to_tensor(image, dtype = tf.float32)
    image= image/255.0
    shape = tf.cast(tf.shape(image)[:-1], tf.float32)
    long_dim = max(shape)
    scale = max_dim/long_dim
    new_shape = tf.cast(shape*scale, tf.int32)
    new_image = tf.image.resize(image, new_shape)
    new_image = new_image[tf.newaxis, :]
    
    return new_image

  #convert tensor to numpy array
  def tensor_toimage(self, tensor):
    tensor =tensor*255
    tensor = np.array(tensor, dtype=np.uint8)
    if np.ndim(tensor)>3:
      assert tensor.shape[0]==1
      tensor=tensor[0]

    return tensor

  def import_art_image(self):
    self.style_im = cv2.imread(self.art_img_path)
    self.style_im = cv2.cvtColor(self.style_im, cv2.COLOR_BGR2RGB)
    self.style_im = self.image_read(self.style_im)

  def process_video(self):
    print("DEBUG: Inside process video")
    self.import_art_image()

    cap = cv2.VideoCapture(self.video_path)
    ret, frame = cap.read()

    # Ensure the frame was successfully read
    if not ret:
        print("Error reading video frame")
        return

    frame_width = self.image_read(frame)[0].shape[1]
    frame_height = self.image_read(frame)[0].shape[0]

    # Get the FPS of the input video
    fps = cap.get(cv2.CAP_PROP_FPS)
    print("Original FPS: ", fps)

    output_path = os.path.dirname(self.video_path) + '/NEST_' + os.path.splitext(os.path.basename(self.video_path))[0] + ".mp4"
    print("Output Path : ", output_path)

    # Use the original FPS for the output video
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

    while True:
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = self.image_read(frame)

            stylized_frame = hub_model(tf.constant(frame), tf.constant(self.style_im))[0]
            image = self.tensor_toimage(stylized_frame)

            # Convert back to BGR for OpenCV and ensure proper frame size
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            image = cv2.resize(image, (frame_width, frame_height))

            out.write(image)
        else:
            break

    cap.release()
    out.release()
    print("Process Complete")
    return output_path




# i_path = '/home/om/Desktop/Nest-Neural-Style-Transfer/Data/Paul_Cezanne_22.jpg'
# v_path = '/home/om/Desktop/Nest-Neural-Style-Transfer/new_V.mp4'

# vp = Video_Processing(i_path, v_path)
# vp.process_video()