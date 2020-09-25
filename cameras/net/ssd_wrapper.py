import glob
import os
import time
import sys

import torch
from PIL import Image
import PIL.ImageFont as ImageFont
from vizer.draw import draw_boxes
import argparse
import numpy as np
import cv2

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#print(sys.path)

from ssd.config import cfg
from ssd.data.datasets import COCODataset, VOCDataset
from ssd.data.transforms import build_transforms
from ssd.modeling.detector import build_detection_model
from ssd.utils import mkdir
from ssd.utils.checkpoint import CheckPointer

class SSD():
    instance = False


    def __init__(self, config_file, dataset_type,
                    weight,score_threshold=0.5, targets=["person"]):
         if SSD.instance is False:
            SSD.instance = True
            self.update_config(config_file,dataset_type,weight,score_threshold,targets)

    def update_score_threshold(self, score_threshold):
        self.score_threshold = score_threshold

    def update_config(self, targets):
        self.target_labels = []
        if targets is None:
            self.target_labels = [i for i in range(len(self.class_names))]
        else:
            for idx in range(len(self.class_names)):
                if self.class_names[idx] in targets:
                    self.target_labels.append(idx)

    def update_config(self,config_file, dataset_type,
                      weight,score_threshold=0.5, targets=["person"]):
        if dataset_type == "voc":
            self.class_names = VOCDataset.class_names
        elif dataset_type == "coco":
            self.class_names = COCODataset.class_names
        else:
            raise NotImplementedError('Not implemented now.')
        self.target_labels = []
        if targets is None:
            self.target_labels = [i for i in range(len(self.class_names))]
        else:
            for idx in range(len(self.class_names)):
                if self.class_names[idx] in targets:
                    self.target_labels.append(idx)
        self.cfg = cfg
        self.cfg.merge_from_file(config_file)
        self.cfg.freeze()
        print("Loaded configuration file {}".format(config_file))
        with open(config_file, "r") as cf:
            config_str = "\n" + cf.read()
#            print(config_str)
#        print("Running SSD with config:\n{}".format(self.cfg))
        
        self.device = torch.device(self.cfg.MODEL.DEVICE)
        self.model = build_detection_model(self.cfg)
        self.model = self.model.to(self.device)
        self.checkpointer = CheckPointer(self.model)
        self.checkpointer.load(weight)
        self.cpu_device = torch.device("cpu")
        self.score_threshold = score_threshold
        self.transforms = build_transforms(self.cfg,is_train=False)
        self.model.eval()

    def predict(self,img):
        height, width = img.shape[:2]
        images = self.transforms(img)[0].unsqueeze(0)
        with torch.no_grad():
            result = self.model(images.to(self.device))[0]
        result = result.resize((width,height)).to(self.cpu_device).numpy()
        boxes, labels, scores = result['boxes'], result['labels'], result['scores']
        indices = np.zeros(labels.shape)
        for label in self.target_labels:
            new_indices = labels == label
            indices = indices + new_indices
        indices = indices > 0
        boxes = boxes[indices]
        labels = labels[indices]
        scores = scores[indices]
        indices = scores > self.score_threshold
        boxes = boxes[indices]
        labels = labels[indices]
        scores = scores[indices]
        
        font = ImageFont.truetype('arial.ttf', 10)
        drawn_image = draw_boxes(img, boxes, labels, scores, self.class_names, font=font).astype(np.uint8)
        drawn_image = self._draw_info(drawn_image,boxes)
        return len(boxes), drawn_image   
      
    def _draw_info(self,img,boxes):
        number = len(boxes)
        word = "Sum:{}".format(number)
        cv2.putText(img,word, (0,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 1)
        return img
