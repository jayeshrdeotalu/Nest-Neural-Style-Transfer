import tensorflow as tf
import tensorflow_hub as hub
import matplotlib.pyplot as plt
import numpy as np
import cv2
import PIL

hub_model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')

#read image, convert to tensor, normalize and resize 
def image_read(image):
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
def tensor_toimage(tensor):
  tensor =tensor*255
  tensor = np.array(tensor, dtype=np.uint8)
  if np.ndim(tensor)>3:
    assert tensor.shape[0]==1
    tensor=tensor[0]

  return tensor

style_im = cv2.imread("Data/Wallpaper_3.jpeg")
style_im = cv2.cvtColor(style_im, cv2.COLOR_BGR2RGB)
style_im = image_read(style_im)

cap = cv2.VideoCapture("content.mp4")


#in order to get the size of width and shape of video, we used first frame of video
ret, frame = cap.read()
frame_width = image_read(frame)[0].shape[1]
frame_height= image_read(frame)[0].shape[0]

out = cv2.VideoWriter('Data/output.mp4', cv2.VideoWriter_fourcc(*'XVID'), 10, 
                      (frame_width,frame_height))

while True:
  ret, frame = cap.read()
  if ret == True:
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = image_read(frame)
    stylized_frame = hub_model(tf.constant(frame), tf.constant(style_im))[0]
    image = tensor_toimage(stylized_frame)
    out.write(image)
  else:
    break

cap.release()
out.release()

print("Process Complete")