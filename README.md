# YOLOv5DS

Multi-task yolov5 with detection and segmentation based on [yolov5](https://github.com/ultralytics/yolov5)(branch v6.0)

<p align="center">
<img src="data/images/6f0bbe0e23fc4747a2ae65dbef2a6173.png">
</p>

- [x] decoupled head
- [ ] anchor free
- [x] segmentation head

[README中文](READMECH.md)

## Ablation experiment

All experiments is trained on a small dataset with 47 classes ,2.6k+ images for training and 1.5k+ images for validation:

| model                                          | P     | R     | map@.5 | map@.5:95 |
| ---------------------------------------------- | ----- | ----- | ------ | --------- |
| yolov5s                                        | 0.536 | 0.368 | 0.374  | 0.206     |
| yolov5s+train scrach                           | 0.452 | 0.314 | 0.306  | 0.152     |
| yolov5s+decoupled head                         | 0.555 | 0.375 | 0.387  | 0.214     |
| yolov5s + decoupled head+class balance weights | 0.541 | 0.392 | 0.396  | 0.217     |
| yolov5s + decoupled head+class balance weights | 0.574 | 0.386 | 0.403  | 0.22      |
| yolov5s + decoupled head+seghead               | 0.533 | 0.383 | 0.396  | 0.212     |

The baseline model is yolov5s. triks like decoupled head, add class balance weights all help to improve MAP.

Adding a segmentation head can still get  equivalent MAP as single detection model.



## Training Method

```
python trainds.py
```

<p align="center">
<img src="data/images/Screenshot.png">
</p>

As VOC dataset do not offer the box labels and mask labels for all images, so we forward this model with a detection batch and a segmention batch by turns, and accumulate the gradient , than update the whole model parameters.

## MAP

To compare with the SSD512, we use VOC07+12 training set as the detection training set, VOC07 test data as detection test data, for segmentation ,we use VOC12 segmentation datset as training and test set.

the input size is 512(letter box).

<p align="center">
<img src="data/images/ssd.png">
</p>

| model                | VOC2007 test |
| -------------------- | ------------ |
| SSD512               | 79.8         |
| yolov5s+seghead(512) | 79.2         |

The above results only trained less than 200 epoch, [weights](https://github.com/midasklr/yolov5ds/releases/download/v6.0/yolodsvoc.pt)

## demo

see detectds.py.

<p align="center">
<img src="data/images/2007_000033_yolods.png">
</p>

<p align="center">
<img src="data/images/2007_002046_yolods.png">
</p>

<p align="center">
<img src="data/images/2007_000925_yolods.png">
</p>


## Train custom data

1. Use labelme to label box and mask on your dataset;

   the box label format is voc, you can use voc2yolo.py to convert to yolo format,

   the mask label  is json files , you should convert to mask .png image labels,like VOC2012 segmentation labels.

2. see [how to arrange your detection dataset with yolov5](https://github.com/ultralytics/yolov5/wiki/Train-Custom-Data) , then arrange your segmentation dataset same as yolo files , see data/voc.yaml:

   ```
   
   # Train/val/test sets as 1) dir: path/to/imgs, 2) file: path/to/imgs.txt, or 3) list: [path/to/imgs1, path/to/imgs2, ..]
   path: .  # dataset root dir
   train: VOC/det/images/train  # train images (relative to 'path') 118287 images
   val: VOC/det/images/test  # train images (relative to 'path') 5000 images
   road_seg_train: VOC/seg/images/train   # road segmentation data
   road_seg_val: VOC/seg/images/val
   
   # Classes
   nc: 20  # number of classes
   segnc: 20
   
   names: ['aeroplane', 'bicycle', 'bird', 'boat',
              'bottle', 'bus', 'car', 'cat', 'chair',
              'cow', 'diningtable', 'dog', 'horse',
              'motorbike', 'person', 'pottedplant',
              'sheep', 'sofa', 'train', 'tvmonitor']  # class names
   
   segnames: ['aeroplane', 'bicycle', 'bird', 'boat',
              'bottle', 'bus', 'car', 'cat', 'chair',
              'cow', 'diningtable', 'dog', 'horse',
              'motorbike', 'person', 'pottedplant',
              'sheep', 'sofa', 'train', 'tvmonitor']
   ```

   3. change the config in trainds.py and :

   ```
   python trainds.py 
   ```

   4. test image folder with :

      ```
      python detectds.py
      ```

      


## Reference

1. [YOLOP: You Only Look Once for Panoptic Driving Perception](https://arxiv.org/abs/2108.11250)
2. [yolov5]( https://github.com/ultralytics/yolov5)

## Blogs

1. https://blog.csdn.net/IEEE_FELLOW/article/details/121912670?spm=1001.2014.3001.5502
2. https://blog.csdn.net/qq_57076285/article/details/124265887
3. https://blog.csdn.net/sadjhaksdas/article/details/125762260
4. https://blog.csdn.net/LWD19981223/article/details/125921793
