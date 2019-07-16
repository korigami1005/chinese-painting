import tensorflow as tf
from skimage import transform
from skimage import data
import matplotlib.pyplot as plt
import os
import numpy as np
from skimage.color import rgb2gray
import random
from keras.models import Sequential 
from keras.layers import Conv2D  # Convolution Operation
from keras.layers import MaxPooling2D # Pooling
from keras.layers import Flatten
from keras.layers import Dense,Dropout # Fully Connected Networks
from keras.regularizers import l2
import pandas as pd
import keras
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

#model D
epochs = 20
batch_size = 32
input_shape = (128,128,3)
model_D = Sequential([
    Conv2D(16, (1,1), input_shape=input_shape,padding = 'same',activation = 'relu'),
    Conv2D(32, (3,3),activation = 'relu',kernel_regularizer=l2(0.01),padding = 'same'),
    Conv2D(32, (3,3),activation = 'relu',kernel_regularizer=l2(0.01),padding = 'same'),
    MaxPooling2D(pool_size=(2,2)),
    Conv2D(64, (3,3),activation = 'relu',kernel_regularizer=l2(0.01),padding = 'same'),
    Conv2D(64, (3,3),activation = 'relu',kernel_regularizer=l2(0.01),padding = 'same'),
    MaxPooling2D(pool_size=(2,2)),
    Flatten(),
    Dense(128,activation= 'relu'),
    Dropout(0.3),
    Dense(128,activation= 'relu'),
    Dense(15, activation='softmax')
])
model_D.summary()
model_D.compile(loss=keras.losses.categorical_crossentropy,
                 optimizer=keras.optimizers.adagrad(),
                 metrics=['accuracy'])
history_01_1 = model_D.fit(Btrain_x,Btrain_y,
                         batch_size = batch_size,
                         epochs=epochs,
                         verbose=1,
                         validation_data=(Bval_x,Bval_y))