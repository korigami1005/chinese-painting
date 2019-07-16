# -*- coding: UTF-8 -*-
#套件引用
import os
from os import walk
from os.path import join
import shutil
import time
import pandas
import random
#GUI視窗
import tkinter as tk
from tkinter import messagebox as alertbox
from tkinter import *
from tkinter import filedialog
#圖片基本處理套件
import matplotlib
matplotlib.use('tkagg')
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image,ImageTk
#切割套件
from skimage.segmentation import slic,mark_boundaries
from skimage.util import img_as_float
#檔案處理
import tensorflow as tf
from skimage import transform,data
os.environ['KMP_DUPLICATE_LIB_OK']='TRUE'
#變數
screen_width = 800
screen_height = 500
output_width = round(screen_width/3)
output_height = (screen_height-80)
type_list = ['人物','山水','五穀','水中動植物','走獸','車','果蔬','花草','建築','草蟲','翎毛','船','器用','樹木','無法辨識']
type_list = ['human','landscape','grains','aquatic pleats and animals','animals',
         'cars','fruit and vegetsble','flowers','building','insects'
         ,'birds','boats','tools','trees','undefined']
list_color =[(0.8, 0, 0),
 (0.6, 0, 0),
 (1, 0.6, 0.2),
 (0.8, 0.4, 0.6),
 (0, 0.4, 0.6),
 (0.2, 1, 1),
 (0, 0.2, 0.4),
 (0.8, 0, 0.4),
 (0.4, 0.4, 0.8),
 (1, 0.2, 0.6),
 (0.2, 0, 1),
 (0.4, 0.6, 0.6),
 (0.4, 0.6, 1),
 (0.8, 0.4, 0.8),
 (0.6, 0.8, 0.6)]



class index():
	def main(master):
		#畫部區
		global canvas_left
		global canvas_mid
		global canvas_right
		canvas_left = Canvas(master,height=screen_height-80,width=screen_width/3)
		canvas_left.place(x=0,y=0)
		canvas_mid = Canvas(master,height=screen_height-80,width=screen_width/3)
		canvas_mid.place(x=screen_width/3,y=0)
		canvas_right = Canvas(master,height=screen_height-80,width=screen_width/3)
		canvas_right.place(x=screen_width*2/3,y=0)

		#按扭區
		btn_choose = Button(master,text='選擇圖片',command=issue.isu_choose,font = ('Helvetica','30'))
		btn_slic = Button(master,text='SLIC分割',command=issue.isu_slic,font = ('Helvetica','30'))
		btn_analysis = Button(master,text='分析圖片',command=issue.isu_analysis,font = ('Helvetica','30'))
		btn_result = Button(master,text='結果顯示',command=issue.isu_result,font = ('Helvetica','30'))
		btn_color = Button(master,text='顏色參考',command=issue.isu_color,font = ('Helvetica','30'))
		btn_choose.place(x=0,y=screen_height-80,width=(screen_width)*0.2,height=80)
		btn_slic.place(x=(screen_width)*0.2,y=screen_height-80,width=(screen_width)*0.2,height=80)
		btn_analysis.place(x=(screen_width)*0.4,y=screen_height-80,width=(screen_width)*0.2,height=80)
		btn_result.place(x=(screen_width)*0.6,y=screen_height-80,width=(screen_width)*0.2,height=80)
		btn_color.place(x=(screen_width)*0.8,y=screen_height-80,width=screen_width*0.2,height=80)

class issue():
	def isu_choose():
		global file_path
		file_path = filedialog.askopenfilename()
		#print(file_path)
		im = Image.open(file_path)
		jpg_path = join(os.getcwd(),'raw.jpg')
		if file_path[-3:]=='png':
			bg = Image.new("RGB", im.size, (255,255,255))
			bg.paste(im,im)
			bg.save(jpg_path)
		else:
			im.save(jpg_path)
		file_path = jpg_path
		#print(file_path)
		#print(im.width,im.height)
		im_w = im.width
		im_h = im.height
		if (im_h/im_w) >= (output_height/output_width):
			trans_h = output_height
			trans_w = round(im_w*output_height/im_h)
			bias_x = (output_width - trans_w)/2
			bias_y = 0
		else:
			trans_h = round(im_h*output_width/im_w)
			trans_w = output_width
			bias_x = 0
			bias_y = (output_height - trans_h)/2
		#print(trans_w,trans_h)
		im = im.resize((trans_w, trans_h), Image.ANTIALIAS)
		canvas_left.image = ImageTk.PhotoImage(im)
		canvas_left.create_image(bias_x,bias_y,image=canvas_left.image,anchor='nw')
		#canvas_mid.create_image(bias_x,bias_y,image=canvas_left.image,anchor='nw')
		#canvas_right.create_image(bias_x,bias_y,image=canvas_left.image,anchor='nw')
		alertbox.showinfo('通知','載入完畢')
		pass
	def isu_slic():
		mix_path = slic_algorithm.mix(file_path)
		im = Image.open(mix_path)
		#print(im.width,im.height)
		im_w = im.width
		im_h = im.height
		if (im_h/im_w) >= (output_height/output_width):
			trans_h = output_height
			trans_w = round(im_w*output_height/im_h)
			bias_x = (output_width - trans_w)/2
			bias_y = 0
		else:
			trans_h = round(im_h*output_width/im_w)
			trans_w = output_width
			bias_x = 0
			bias_y = (output_height - trans_h)/2
		#print(trans_w,trans_h)
		im = im.resize((trans_w, trans_h), Image.ANTIALIAS)
		canvas_mid.image = ImageTk.PhotoImage(im)
		canvas_mid.create_image(bias_x,bias_y,image=canvas_mid.image,anchor='nw')
		global local
		local = './proper/'
		if os.path.isdir(local):
			shutil.rmtree(local)
		if not os.path.isdir(local):
			os.mkdir(local)
		slic_algorithm.cut_image(file_path,local)
		alertbox.showinfo('通知','分割完畢')
	def isu_analysis():
		global pred
		file_path = '/Users/korigami/Desktop/0702/raw.jpg'
		model_name = '98.h5'
		#model_name = filedialog.askopenfilename()
		model = tf.contrib.keras.models.load_model(model_name)
		local = './proper/'
		jpgs = analysis_data.load_data(local)
		images = analysis_data.trans_128(jpgs)
		pred = model.predict_classes(images)
		#print(pred)
		analysis_data.draw_color(file_path,pred)
		alertbox.showinfo('通知','分析完畢')
		pass
	def isu_result():
		count = np.zeros(15)
		for i in range(pred.shape[0]):
			count[pred[i]] = count[pred[i]] + 1
		#print(count)
		type_str = ''
		for i in range(15):
			if count[i] > 0:
				type_str = type_str + type_list[i] +';'
		alertbox.showinfo('通知','類別有：'+type_str)
		im = Image.open('color.jpg')
		im_w = im.width
		im_h = im.height
		if (im_h/im_w) >= (output_height/output_width):
			trans_h = output_height
			trans_w = round(im_w*output_height/im_h)
			bias_x = (output_width - trans_w)/2
			bias_y = 0
		else:
			trans_h = round(im_h*output_width/im_w)
			trans_w = output_width
			bias_x = 0
			bias_y = (output_height - trans_h)/2
		im = im.resize((trans_w, trans_h), Image.ANTIALIAS)
		canvas_right.image = ImageTk.PhotoImage(im)
		canvas_right.create_image(bias_x,bias_y,image=canvas_right.image,anchor='nw')
	def isu_color():
		im = Image.open('color_list.jpg')
		im_w = im.width
		im_h = im.height
		if (im_h/im_w) >= (output_height/output_width):
			trans_h = output_height
			trans_w = round(im_w*output_height/im_h)
			bias_x = (output_width - trans_w)/2
			bias_y = 0
		else:
			trans_h = round(im_h*output_width/im_w)
			trans_w = output_width
			bias_x = 0
			bias_y = (output_height - trans_h)/2
		im = im.resize((trans_w, trans_h), Image.ANTIALIAS)
		canvas_left.image = ImageTk.PhotoImage(im)
		canvas_left.create_image(bias_x,bias_y,image=canvas_left.image,anchor='nw')
		#canvas_mid.create_image(bias_x,bias_y,image=canvas_left.image,anchor='nw')
		#canvas_right.create_image(bias_x,bias_y,image=canvas_left.image,anchor='nw')
		pass

class slic_algorithm():
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
	def max_min(array,number):
		x_list = []
		y_list = []
		for i in range(array.shape[0]):
			for j in range(array.shape[1]):
				if array[i][j] == number:
					if i not in x_list:
						x_list.append(i)
					if j not in y_list:
						y_list.append(j)
		return (min(x_list),max(x_list),min(y_list),max(y_list))
	def img_generate(img_float,img_slic,number):
		(a,b,c,d) = slic_algorithm.max_min(img_slic,number)
		img_sep = np.zeros((b-a+1,d-c+1,3))
		for i in range(img_sep.shape[0]):
			for j in range(img_sep.shape[1]):
				if img_slic[a+i][c+j] == number:
					img_sep[i][j] = img_float[a+i][c+j]
		return img_sep
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

class analysis_data():
	def load_data(path):
		im_path = []
		for a,b,c in os.walk(path):
			im_path.append(c)
		im = []
		for i in range(len(im_path[0])):
			im.append(os.path.join(path,im_path[0][i]))
		images = []
		for i in range(len(im)):
			images.append(data.imread(im[i]))
		return images
	def trans_128(imgs):
		p_128 = [transform.resize(image, (128, 128)) for image in imgs]
		p_arr = np.array(p_128)
		images = (p_arr - p_arr.min())/(p_arr.max() - p_arr.min())
		return images
	def draw_color(file,pred):
		im = Image.open(file)
		im_w = im.width
		im_h = im.height
		im_float = img_as_float(im)
		color = np.zeros((im_h,im_w,3))
		side_x = round(im_w/128)
		side_y = round(im_h/128)
		a = side_x * side_y
		b = 1
		c = 10
		im_slic = slic(im_float,n_segments=a,sigma=b,compactness=c)
		sep_max = np.max(im_slic)
		for i in range(im_h):
			for j in range(im_w):
				area_num = im_slic[i][j]
				type_num = pred[area_num]
				color[i][j] = list_color[type_num]
		color = mark_boundaries(color,im_slic,color=(1,1,1))
		plt.imsave('color.jpg',color)
		pass



#系統初始參數
if __name__ == '__main__':
	root = tk.Tk()
	root.title('國畫主題辨識器')
	root.geometry(str(screen_width) + 'x' + str(screen_height))
	index.main(root)
	root.mainloop() 
