import tensorflow as tf
from skimage import transform
from skimage import data
import numpy as np
from skimage.color import rgb2gray
import random
from keras.layers import Conv2D  # Convolution Operation
import pandas as pd
import keras
import os
import matplotlib.pyplot as plt
from keras import applications
from keras.preprocessing.image import ImageDataGenerator
from keras import optimizers
from keras.models import Sequential, Model 
from keras.layers import Dropout, Flatten, Dense, GlobalAveragePooling2D
from keras import backend as k 
from keras.callbacks import ModelCheckpoint, LearningRateScheduler, TensorBoard, EarlyStopping
ROOT_PATH = '/Users/korigami/Desktop/Train_step改/'
os.environ['KMP_DUPLICATE_LIB_OK']='TRUE'
def load_data(path):
    folder =[]
    images = []
    labels = []
    for a,b,c in os.walk(ROOT_PATH):
        if a.split('/')[-1][0:5] == 'train':
            folder.append(a)
    for i in range(len(folder)):
        #print(folder[i])
        one_img = []
        one_csv = []
        for a1,b1,c1 in os.walk(folder[i]):
            for f in c1:
                if f.split('.')[-1] == 'jpg':
                    one_img.append(os.path.join(a1,f))
                elif f.split('.')[-1] == 'csv':
                    one_csv.append(os.path.join(a1,f))
        for j in range(len(one_img)):
            images.append(data.imread(one_img[j]))
        csv_file = one_csv[0]
        ooo = pd.read_csv(csv_file,sep=';')
        #print(ooo.shape[0])
        for i in range(ooo.shape[0]):
            labels.append(ooo['Label'][i])
    print('Load Suecced')
    return images,labels
ppee,pee = load_data(ROOT_PATH)
p_128 = [transform.resize(image, (128, 128)) for image in ppee]
p_arr = np.array(p_128)
images = (p_arr - p_arr.min())/(p_arr.max() - p_arr.min())
import keras
pee_new = np.array(pee)
pee_new = pee_new -1
num_classes = 15
labels = keras.utils.to_categorical(pee_new,num_classes)
goods = []
for i in range(9385):
    goods.append((images[i],pee_new[i]))
np.random.shuffle(goods)
train_x = []
train_y = []
val_x = []
val_y = []
for i in range(6385):
    train_x.append(goods[i][0])
    train_y.append(goods[i][1])
for i in range(6385,7885):
    val_x.append(goods[i][0])
    val_y.append(goods[i][1])
train_x = np.array(train_x)
train_y = np.array(train_y)
train_y = keras.utils.to_categorical(train_y,15)
val_x = np.array(val_x)
val_y = np.array(val_y)
val_y = keras.utils.to_categorical(val_y,15)

img_width, img_height = 128, 128
nb_train_samples = 9385
batch_size = 16
epochs = 20

model = applications.VGG19(weights = "imagenet", include_top=False, input_shape = (img_width, img_height, 3))
for layer in model.layers[:22]:
    layer.trainable = True
for layer in model.layers[:21]:
    layer.trainable = False
x = model.output
x = Flatten()(x)
x = Dense(1024, activation="relu")(x)
x = Dropout(0.5)(x)
x = Dense(1024, activation="relu")(x)
predictions = Dense(15, activation="softmax")(x)
model_final = Model(input = model.input, output = predictions)
model_final.compile(loss = "categorical_crossentropy", 
                    optimizer = optimizers.SGD(lr=0.0001, momentum=0.9), 
                    metrics=["accuracy"])
history = model_final.fit(train_x,train_y,
                         batch_size = batch_size,
                         epochs=epochs,
                         verbose=1,
                         validation_data=(val_x,val_y))
