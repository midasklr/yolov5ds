import shutil
import os

trainval = ['train','val']

for it in trainval:
    with open("minidet/ImageSets/Main/{}.txt".format(it),'r') as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip()
        shutil.copy("minidet/JPEGImages/{}.jpg".format(line),"Mini/images/{}/{}.jpg".format(it,line))




