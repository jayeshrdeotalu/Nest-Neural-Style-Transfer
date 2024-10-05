import tensorflow as tf
import tensorflow_hub as hub
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os

hub_model = hub.load('NST_Model')
print("Model loaded successfully from the local directory!")

class ImageProcessing:

    def __init__(self, art_img_path, image_path):

        print("DEBUG: INSIDE INIT")
        self.art_img_path = art_img_path
        self.image_path = image_path
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


    def process_image(self):

        print("DEBUG: Inside process image")
        self.import_art_image()

        print("DEBUG: art img path : ", self.art_img_path)
        print("DEBUG: input img path : ", self.image_path)

        # Read the input image
        input_image = cv2.imread(self.image_path)
        
        if input_image is None:
            print("ERROR: Could not load input image.")
            return None

        # Convert the image to RGB (TensorFlow works with RGB)
        input_image_rgb = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)

        # Resize/prepare image if needed (assuming self.image_read handles resizing or preprocessing)
        preprocessed_image = self.image_read(input_image_rgb)[0]

        # Add a batch dimension (to make it 4D: [1, height, width, channels])
        preprocessed_image = tf.expand_dims(preprocessed_image, axis=0)

        # Perform neural style transfer
        stylized_image = hub_model(tf.constant(preprocessed_image), tf.constant(self.style_im))[0]

        # Remove the batch dimension
        stylized_image = tf.squeeze(stylized_image, axis=0)

        # Convert the stylized image tensor back to an image
        output_image = self.tensor_toimage(stylized_image)

        # Define the output path for the stylized image
        output_path = os.path.dirname(self.image_path) + '/NEST_' + os.path.splitext(os.path.basename(self.image_path))[0] + ".jpg"
        print("Output Path : ", output_path)

        # Save the stylized image
        cv2.imwrite(output_path, output_image)

        print("Process Complete")
        return output_path




# i_path = '/home/om/Desktop/Nest-Neural-Style-Transfer/Data/Paul_Cezanne_22.jpg'
# v_path = '/home/om/Desktop/Nest-Neural-Style-Transfer/aaa_1.jpg'

# vp = ImageProcessing(i_path, v_path)
# vp.process_image()