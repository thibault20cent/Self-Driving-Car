#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import cv2

def decoupageSegment(image,N) : #image à découper en N sous images
    IMAGE_H, IMAGE_W = image.shape[:2] #taille de l image
    list = []
    tailleSegment = IMAGE_H / N
    for i in range (N) :
        segment = image [i*tailleSegment : (i+1)*tailleSegment, 0:IMAGE_W]
        list.append(segment)
    return list

def concatene(list):
    nbSegments = len(list)
    taille_H_seg, taille_W_seg = list[0].shape[:2]
    height = taille_H_seg * nbSegments
    width = taille_W_seg
    newImg = np.empty((height, width, 3), dtype = np.uint8)
    for i in range(nbSegments) :
        newImg[i*taille_H_seg : (i+1)*taille_H_seg, 0:width] = list[i]
    return newImg
