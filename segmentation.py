import numpy as np
import cv2

def preProcessingHoughLine(img):
    #Detection de contours
    edges = cv2.Canny(img,50,150,apertureSize = 3)
    kernel = np.ones((1,1),np.uint8)
    dilatation = cv2.dilate(edges,kernel,iterations = 1)
    erode = cv2.erode(img,kernel,iterations = 1)
    return dilatation

def houghLine(img, preProcessed):
    color = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    meanSin=0
    meanCos=0
    meanAngle=-1
    Droite = True
    try:
        lines = cv2.HoughLines(preProcessed,rho = 1,theta = 2*np.pi/180,threshold = 80)
        for i in range(len(lines)):
            for rho,theta in lines[i]:
                #print('rho theta', rho, theta)
                a = np.cos(theta)
                b = np.sin(theta)
                #print('cos', a)
                x0 = a*rho
                y0 = b*rho
                x1 = int(x0 + 1000*(-b))
                y1 = int(y0 + 1000*(a))
                x2 = int(x0 - 1000*(-b))
                y2 = int(y0 - 1000*(a))
                cv2.line(color,(x1,y1),(x2,y2),(0,0,255),2)
                meanSin += b
                meanCos += a
        if len(lines) != 0:
            if meanCos < 0:
                meanAngle = np.arcsin(meanSin/len(lines)) + np.pi/2
            else:
                meanAngle = np.pi/2-np.arcsin(meanSin/len(lines))

    except Exception as e:
        print 'There is no lines to be detected!'
    return (color,meanAngle)

def Segmentation(img):
    #segmentation couleur
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.uint8([20, 80, 20])
    upper = np.uint8([40, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)
    res = cv2.bitwise_and(img,img, mask= mask)
    
    #Smoothing avec un filtre gaussien
    kernel_size = 3
    blur = cv2.GaussianBlur(mask, (kernel_size, kernel_size), 0)
    #cv2.imshow('smooth1',blur)
    return blur

def Morphology(img):
    #Mophology
    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    return opening

def approxPoly(img,precision,bool):
    canvas = np.zeros(img.shape, np.uint8)
    im2,contours,hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    display = cv2.cvtColor(canvas, cv2.COLOR_GRAY2BGR)
    for cnt in contours:
        epsilon = precision*cv2.arcLength(cnt,bool)
        approx = cv2.approxPolyDP(cnt,epsilon,bool)
        #print('\n')
        cv2.drawContours(display, [approx], -1, (255, 255, 255), 3)
    return display

def detectionLigneStop(img):
    return img
