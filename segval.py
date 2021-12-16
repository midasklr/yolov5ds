# YOLOv5 🚀 by Ultralytics, GPL-3.0 license
"""
Validate a trained YOLOv5 model accuracy on a custom dataset

Usage:
    $ python path/to/val.py --data coco128.yaml --weights yolov5s.pt --img 640
"""

import argparse
import json
import os
import sys
from pathlib import Path
from threading import Thread
from utils.general import LOGGER

import numpy as np
import torch
from tqdm import tqdm



class AverageMeter(object):
    """Computes and stores the average and current value"""

    def __init__(self):
        self.initialized = False
        self.val = None
        self.avg = None
        self.sum = None
        self.count = None

    def initialize(self, val, weight):
        self.val = val
        self.avg = val
        self.sum = val * weight
        self.count = weight
        self.initialized = True

    def update(self, val, weight=1):
        if not self.initialized:
            self.initialize(val, weight)
        else:
            self.add(val, weight)

    def add(self, val, weight):
        self.val = val
        self.sum += val * weight
        self.count += weight
        self.avg = self.sum / self.count

    def value(self):
        return self.val

    def average(self):
        return self.avg


def get_confusion_matrix(label, pred, size, num_class, ignore=-1):
    """
    Calcute the confusion matrix by given label and pred
    """
    output = pred.cpu().numpy().transpose(0, 2, 3, 1)
    seg_pred = np.asarray(np.argmax(output, axis=3), dtype=np.uint8)
    seg_gt = np.asarray(
        label.cpu().numpy()[:, :size[-2], :size[-1]], dtype=np.int)

    ignore_index = seg_gt != ignore
    seg_gt = seg_gt[ignore_index]
    seg_pred = seg_pred[ignore_index]

    index = (seg_gt * num_class + seg_pred).astype('int32')
    label_count = np.bincount(index)
    confusion_matrix = np.zeros((num_class, num_class))

    for i_label in range(num_class):
        for i_pred in range(num_class):
            cur_index = i_label * num_class + i_pred
            if cur_index < len(label_count):
                confusion_matrix[i_label,
                                 i_pred] = label_count[cur_index]
    return confusion_matrix


def validate(testloader, model, numcls, criterion):
    model.eval()
    ave_loss = AverageMeter()
    confusion_matrix = np.zeros((numcls, numcls))

    s = ('%11s' * 3) % ('Images', 'Ave Loss', 'mIOU')
    pbar = tqdm(testloader, desc=s, bar_format='{l_bar}{bar:10}{r_bar}{bar:-10b}')  # progress bar

    with torch.no_grad():
        for idx, batch in enumerate(pbar):
            image, label, _, _ = batch
            size = label.size()
            image = image.cuda().float()/255
            label = label.long().cuda()

            out = model(image)
            pred = out[1]
            losses = criterion(pred, label)

            confusion_matrix += get_confusion_matrix(label, pred, size, numcls, 255)

            loss = losses.mean()

            reduced_loss = loss
            ave_loss.update(reduced_loss.item())

        confusion_matrix = torch.from_numpy(confusion_matrix).cuda()
        reduced_confusion_matrix = confusion_matrix
        confusion_matrix = reduced_confusion_matrix.cpu().numpy()

        pos = confusion_matrix.sum(1)
        res = confusion_matrix.sum(0)
        tp = np.diag(confusion_matrix)
        IoU_array = (tp / np.maximum(1.0, pos + res - tp))
        mean_IoU = IoU_array.mean()
    LOGGER.info('%11g' * 3 % (len(testloader), ave_loss.average(), mean_IoU))

    return ave_loss.average(), mean_IoU, IoU_array
