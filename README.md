## Data Parser for Open Images
These scripts were written in order to download annotations from Google's Open Images dataset and convert them into a simple csv format.
If you want to have a look at the publicly available data, you can go to the following link
https://storage.googleapis.com/openimages/web/visualizer/index.html?set=train&type=segmentation&r=false&c=%2Fm%2F025rp__

Annotations come in several formats, including
a) 'detection' (bounding boxes)
b) 'segmentation' (masks).

In here, two data parsers are included for the aforementioned two annotation formats.

Once you have taken a look at the data and chosen the class of objects you need annotations for, you then have to download the data.
## 1) Download Data along with bouding box annotations
```bash
oi_download_images --csv_dir ~/Workspaces/michele/open_images/ --base_dir ~/Workspaces/michele/open_images/ --labels 'Traffic sign'
```
This step will download
- at csv_dir:
-- train-annotations-bbox.csv: a csv file containing the training set bounding box annotations for the label you have chosen
-- test-annotations-bbox.csv: a csv file containing the test set bounding box annotations for the label you have chosen
-- val-annotations-bbox.csv: a csv file containing the val set bounding box annotations for the label you have chosen
-- class-description-boxable.csv: labels map
- at base_dir
-- the images will be saved in a folder named after the label name

## 2a) Parse bounding box annotations
```bash
python data_parser_bb.py '/m/01mqdt' traffic_sign '/home/raspect/Workspaces/michele/oiv6/traffic sign/images' '/home/raspect/Workspaces/michele/oiv6/train-annotations-bbox.csv'
```
where:

map_label = sys.argv[1] # get the map label from class-description-boxable.csv
label_name = sys.argv[2] # match the label name with map label from class-description-boxable.csv
images_dir = sys.argv[3] # dir where the images you are parsing annotations for has been stored
file_path = sys.argv[4] # file path of csv file with annotations

## 2b) Download segmentation annotations
Download segmentations from
https://storage.googleapis.com/openimages/web/download.html

alternatively, for datasets 0,1,2,3,4,5,6,7,8,9,A,B,C,D,E,F run in terminal

```bash
mkdir masks_label_name
cd masks_label_name
wget https://storage.googleapis.com/openimages/v5/train-masks/train-masks-0.zip
unzip train-masks-0.zip
```

## 3b) Parse segmentation annotations
```bash
python data_parser_mask.py '/m/01mqdt' traffic_sign '/home/raspect/Workspaces/michele/open_images/traffic sign/images/' '/home/raspect/Workspaces/michele/open_images/masks/' '/home/raspect/Workspaces/michele/open_images/vismasks/'
```

where:
map_label = sys.argv[1] # get the map label from class-description-boxable.csv
label_name = sys.argv[2] # match the label name with map label from class-description-boxable.csv
images_dir = sys.argv[3] # dir where the images you are parsing annotations for has been stored
masks_dir =  sys.argv[4] # dir where masks are stored
vis_masks_dir = sys.argv[5] # dir where to store visualization of masks on image
