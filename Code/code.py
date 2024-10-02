from keras.applications.vgg16 import VGG16
shape = (224,224)
vgg = VGG16(input_shape=shape,weights='imagenet',include_top=False)