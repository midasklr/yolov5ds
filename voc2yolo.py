#coding=utf-8
import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join

sets=[('VOC2007', 'test')]
#sets=[('VOC2007', 'trainval'),('VOC2012', 'trainval')]
# sets=[('2007','train')]

classes = ['aeroplane', 'bicycle', 'bird', 'boat',
           'bottle', 'bus', 'car', 'cat', 'chair',
           'cow', 'diningtable', 'dog', 'horse',
           'motorbike', 'person', 'pottedplant',
           'sheep', 'sofa', 'train', 'tvmonitor']

print('class number:',len(classes))
VOCPath = 'VOCdevkit'


with open("voc.names","w") as fw:
    for item in classes:
        fw.writelines(item+"\n")

def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(year, image_id):
#    print(image_id)
    in_file = open('%s/%s/Annotations/%s.xml'%(VOCPath, year, image_id))
    out_file = open('%s/%s/labels/%s.txt'%(VOCPath, year, image_id), 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    if w == 0 or h == 0:
        print("bad image :",in_file)

    for obj in root.iter('object'):
        #difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes:# or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        if bb[2] ==0 or bb[3] == 0:
            continue
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

wd = getcwd()

for year, image_set in sets:
    if not os.path.exists('%s/%s/labels/'%(VOCPath, year)):
        os.makedirs('%s/%s/labels/'%(VOCPath, year))
    image_ids = open('%s/%s/ImageSets/Main/%s.txt'%(VOCPath, year, image_set)).readlines()
    list_file = open('voc_%s.txt'%(image_set), 'w')
    for image_id in image_ids:
        image_id = image_id.strip()
        #try:
        list_file.write('%s/%s/%s/JPEGImages/%s.jpg\n'%(wd, VOCPath, year, image_id))
        convert_annotation(year, image_id)
       # except:
        #    print(image_id)
    list_file.close()
