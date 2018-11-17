#! /usr/bin/env python

import sys
import glob
import re
import os 
import os.path
directory = "/Users/kevinhchon/Documents/_CMU/Research/Cooking/classifier/images/multi-label"

for filename in os.listdir(directory):
    if filename.endswith(".jpg"): 
        #print(os.path.join(directory, filename))
       	#print(filename)
       	'''
       	file_lst = filename.split('.')
       	print(file_lst)
       	image_id_lst = file_lst[0].split('-')
       	image_id = image_id_lst[0]
       	print(image_id)
       	image_rename = str(image_id) + ".jpg"
       	os.rename(directory + "/" + filename, image_rename)
       	'''
       	file_lst = filename.split('.')
       	image_id = file_lst[0]
       	#print(image_id)
       	file_path = "/Users/kevinhchon/Documents/_CMU/Research/Cooking/classifier/image_labels_dir/" + image_id +".jpg.txt"
       	if not os.path.exists(file_path):
       		os.remove(directory + "/" + filename)
       		print("filename removed: ", filename)
