import csv
import pandas as pd
import os
from PIL import Image
import sys

'''
Download Images
oi_download_images --csv_dir ~/Workspaces/michele/open_images/ --base_dir ~/Workspaces/michele/open_images/ --labels Skyscraper
'''

def data_parser_bb(map_label, label_name, images_dir):

    print('parsing', map_label, label_name)
    header_list = ['ImagePath','XMin','YMin','XMax','YMax','LabelName']
    df = pd.DataFrame(columns=header_list)
    count = 0
    with open(file_path) as file:
      csv_reader = csv.reader(file, delimiter=',')
      for line, row in enumerate(csv_reader):
        ImageID,_,LabelName,_,XMin,XMax,YMin,YMax,_,_,_,_,_ = row
        if LabelName == map_label:
            if os.path.isfile(os.path.join(images_dir,ImageID + '.jpg')):
                count += 1
                image = Image.open(os.path.join(images_dir,ImageID + '.jpg'))
                width, height = image.size
                new_row = {'ImagePath':os.path.join(images_dir,ImageID + '.jpg'), \
                            'LabelName':label_name, \
                            'XMin':round(float(XMin)*width), 'XMax':round(float(XMax)*width), \
                            'YMax':round(float(YMax)*height), 'YMin':round(float(YMin)*height)}
                df = df.append(new_row, ignore_index=True)
            else:
                print('File missing:', os.path.join(images_dir,ImageID + '.jpg'))
    print('Images in Dataset:', count)
    print(df)

    #df.to_csv(os.path.join(images_dir,'test.csv'), \
        #header=None, index=False)
    print('--------------------------------------------------------------------')
    print('Annotations saved at: ', os.path.join(os.path.dirname(images_dir), \
        label_name + '_sp_' + os.path.basename(file_path)))
    df.to_csv(os.path.join(os.path.dirname(images_dir), \
        label_name + '_sp_' + os.path.basename(file_path)), \
        header=None, index=False)

if __name__ == '__main__':
    map_label = sys.argv[1]
    label_name = sys.argv[2]
    images_dir = sys.argv[3]
    file_path = sys.argv[4]
    # for example
    #map_label = '/m/01mqdt'
    #label_name = 'traffic_sign'
    #images_dir = '/home/raspect/Workspaces/michele/oiv6/traffic sign/images'
    #file_path = '/home/raspect/Workspaces/michele/oiv6/train-annotations-bbox.csv'
    #file_path = '/home/raspect/Workspaces/michele/oiv6/test-annotations-bbox.csv'
    data_parser_bb(map_label, label_name, images_dir)
