import cv2
import csv
import os
import re
import pandas as pd
from skimage import io
from skimage import measure
import matplotlib.pyplot as plt
import numpy as np
import sys


def bw_scale(file_name, tresh_min, tresh_max):
    image = cv2.imread(file_name)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    (thresh, im_bw) = cv2.threshold(image, tresh_min, tresh_max, 0)
    return (thresh, im_bw)

def edge_detect(masks_dir, file_name, writer, vis_masks_dir, tresh_min=128, tresh_max=255):
    if os.path.isfile(images_dir + file_name.replace('_','').split(map_label.replace('/',''))[0]+'.jpg'):
        print('Found')
        if not os.path.isdir(vis_masks_dir):
            os.mkdir(vis_masks_dir)
        image = cv2.imread(images_dir + file_name.replace('_','').split(map_label.replace('/',''))[0]+'.jpg')
        (thresh, im_bw) = bw_scale(masks_dir + file_name, tresh_min, tresh_max)
        height = cv2.imread(images_dir + file_name.replace('_','').split(map_label.replace('/',''))[0]+'.jpg').shape[0]
        width = cv2.imread(images_dir + file_name.replace('_','').split(map_label.replace('/',''))[0]+'.jpg').shape[1]
        dim = (width, height)
        im_bw = cv2.resize(im_bw, dim)
        #cv2.imwrite('bw_'+file_name, im_bw)
        contours, hierarchy = cv2.findContours(im_bw, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        image = cv2.imread(images_dir + file_name.replace('_','').split(map_label.replace('/',''))[0]+'.jpg')
        cv2.drawContours(image, contours, -1, (0, 0, 255), 3)
        cv2.imwrite(vis_masks_dir + file_name.split('.')[0] + '_cnt.png',image)

        print('saved ', vis_masks_dir + file_name.split('.')[0] + '_cnt.png')
        annotations = []
        for sublist in contours:
            for item in sublist:
                for subitem in item:
                    for coordinate in subitem:
                        annotations.append(coordinate)
        annotations.insert(0, images_dir + file_name.replace('_','').split(map_label.replace('/',''))[0]+'.jpg')
        annotations.append(label_name)
        writer.writerow(annotations)
    else:
        print('image ', images_dir + file_name.replace('_','').split(map_label.replace('/',''))[0]+'.jpg', ' is missing')

def parse_data(map_label, label_name, images_dir, file_names, vis_masks_dir):
    print('parsing', map_label, label_name)
    print('---------------------------------------------------------------------------------')

    with open(os.path.join(os.path.dirname(os.path.dirname(images_dir)), \
        label_name + '_sp_masks.csv'), 'w', newline='') as f:
        writer = csv.writer(f)
        for f in file_names:
            if map_label.replace('/','') in f:
                edge_detect(images_dir, f, writer, vis_masks_dir)

    print('----------------------------------------------------------------------------------')
    print('Annotations saved at:', os.path.join(os.path.dirname(os.path.dirname(images_dir)), \
        label_name + '_sp_masks.csv'))

if __name__ == '__main__':
    map_label = sys.argv[1]
    label_name = sys.argv[2]
    images_dir = sys.argv[3]
    masks_dir =  sys.argv[4]
    vis_masks_dir = sys.argv[5]
    # for example
    # map_label = '/m/0k4j'
    # label_name = 'car'
    # images_dir = '/home/raspect/Workspaces/michele/oiv6/car/images/'
    # masks_dir = '/home/raspect/Workspaces/michele/oiv6/masks/'
    # vis_masks_dir = '/home/raspect/Workspaces/michele/oiv6/vis_masks/vis_masks_car_cnt/'

    included_extensions = ['jpg','jpeg', 'bmp', 'png', 'gif']
    file_names = [fn for fn in os.listdir(masks_dir)
                  if any(fn.endswith(ext) for ext in included_extensions)]

    parse_data(map_label, label_name, masks_dir, file_names, vis_masks_dir)
