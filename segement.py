#基本套件
import os
from os import walk
from os.path import join
#圖片基本處理套件
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
#切割套件
from skimage.segmentation import slic,mark_boundaries
from skimage.util import img_as_float
#取分割範圍
def max_min(array,number):
    x_list = []
    y_list = []
    for i in range (array.shape[0]):
        for j in range(array.shape[1]):
            if array[i][j] == number:
                if i not in x_list:
                    x_list.append(i)
                if j not in y_list:
                    y_list.append(j)
    return(min(x_list),max(x_list),min(y_list),max(y_list))

#產生單張分割圖片
def img_generate(img_float,img_slic,number):
    (a,b,c,d) = max_min(img_slic,number)
    img_sep = np.zeros((b-a+1,d-c+1,3))
    for i in range(img_sep.shape[0]):
        for j in range(img_sep.shape[1]):
            if img_slic[a+i][c+j] == number:
                img_sep[i][j] = img_float[a+i][c+j]
    return img_sep

#分割圖片
def cut_image(file,path):
    im = Image.open(file)
    im_float = img_as_float(im)
    im_w = im.width
    im_h = im.height
    side_x = round(im_w/128)
    side_y = round(im_h/128)
    a = side_x * side_y
    b = 1
    c = 10
    im_slic = slic(im_float,n_segments=a,sigma=b,compactness=c)
    sep_max = np.max(im_slic)
    #sep_max = 3
    for i in range(sep_max+1):
        pic = slic_algorithm.img_generate(im_float,im_slic,i)
        plt.imsave(path+'pic'+str(i)+'.jpg',pic)
    print('分割完成')
    #mix = mark_boundaries(img_float,img_slic,color=(0,0,0))
    #plt.imsave(path+'mix.jpg',mix)
def get_img(path):
    for root, dirs, files in walk(path):
        for f in files:
            fullpath = join(root,f)
            tt = os.path.splitext(f)
            if tt[-1] == '.jpg':
                img_path = fullpath
    print('Get Data')
    return img_path
def mix(file):
    im = Image.open(file)
    im_float = img_as_float(im)
    im_w = im.width
    im_h = im.height
    side_x = round(im_w/128)
    side_y = round(im_h/128)
    a = side_x * side_y
    b = 1
    c = 10
    im_slic = slic(im_float,n_segments=a,sigma=b,compactness=c)
    mix_image = mark_boundaries(im_float,im_slic,color=(0,0,0))
    path = join(os.getcwd(),'mix.jpg')
    plt.imsave(path,mix_image)
    return path

mypath = os.getcwd()
image_seg = get_img(mypath)
local = './paper train/'
if not os.path.isdir(local):
        os.mkdir(local)
mix(image_seg)
cut_image(image_seg,local)