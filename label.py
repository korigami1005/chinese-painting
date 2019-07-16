#產生標籤檔
#套件引用
import pandas as pd
import numpy as np
import os
import csv
from PIL import Image
from skimage.util import img_as_float

def create_file():
	now_path = os.getcwd()
	groups = []
	for dirPath,dirNames,fileNames in os.walk(now_path):
		if str(dirPath).split('/')[-1][:5] == 'train':
			groups.append(dirPath)
	return groups

def create_images(Path):
	jpg_collect = []
	for dirPath,dirNames,fileNames in os.walk(Path):
		for f in fileNames:
			if f[-4:] == '.jpg':
				jpg_collect.append(f)
	return jpg_collect

def create_csv(images,Path):
	img_name = []
	img_width = []
	img_height = []
	img_label = []
	for f in images:
		img_mix = os.path.join(Path,f)
		img_name.append(f)
		img = img_as_float(Image.open(img_mix))
		img_width.append(img.shape[1])
		img_height.append(img.shape[0])
		img_label.append(f[:2])
	dict = {'Filename':img_name,
	'Width':img_width,
	'Height':img_height,
	'Label':img_label}
	pd.DataFrame(dict).to_csv(Path+'/Label.csv',index=False,sep=';',encoding='utf-8')

groups = create_file()
for group in groups:
	images = create_images(group)
	create_csv(images,group)