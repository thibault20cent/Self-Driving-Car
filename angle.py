#!/usr/bin/python
# -*- coding: utf-8 -*-


import numpy as np
import cv2

def transfoAngle (meanAngle) :
    # transformation de radians en degres
    angleDeg = meanAngle * 180 / np.pi
    # remise a zero de l origine (tout droit) et angle + et -
    # le - est a gauche, les + à droite
    angleNorm = - (angleDeg - 90)
    return angleNorm

    
def limAngle (angleNorm) :
    if abs (angleNorm) <= 24 :
        return angleNorm

#Sinon ralentir et tourner à fond
    elif angleNorm < -24 :
        return (-24)
   
# dernier cas : angleNorm > 25
    else :
        return (24)


