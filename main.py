#import sys
#sys.settrace
from segmentation import *
from decoupe import *
from classe_Voiture_GPIO import *
from angle import *
import numpy as np
import cv2

    
def main():
    #test fonctionnement voiture
    p.start(0)
    avancer(0.35,0.5)
    q.start(0)
    tourner(-20, 1)
    tourner(20, 1)
    tourner(0, 1)
    
    #flux video
    cap = cv2.VideoCapture(0)
    cv2.namedWindow('image',cv2.WINDOW_NORMAL)
    choixSegment = 0 #dans le sens logitech de la camera haut =0 et bas = 4
    
    #traitement en boucle
    while(True):
        print('new img')
        ret, img = cap.read()
        if ret == False:
            continue
        img = cv2.resize(img, (960, 540))
        #img_crop = img[0:540, 0:480]
        seg = Segmentation(img_crop)
        morph = Morphology(seg)
        preprocessed = preProcessingHoughLine(morph)
        nbSegments = 3
        poly = approxPoly(preprocessed,0.01,False)
        kernel = np.ones((3,3),np.uint8)
        erode = cv2.erode(poly,kernel,iterations = 1)
        erode = cv2.cvtColor(erode, cv2.COLOR_BGR2GRAY)
        #cv2.imshow('image3',erode)
        list1 = decoupageSegment (morph,nbSegments)
        list2 = decoupageSegment (erode,nbSegments)
        new_list=[]
        for i in range (nbSegments):
            (hL,meanAngle)=houghLine(list1[i], list2[i])
            new_list.append(hL)
            if i == 1:
                #cv2.imshow('imagesup',hL)
                if meanAngle != -1:
                    angleNorm = transfoAngle(meanAngle)
                    angleNormLim = limAngle(angleNorm)
                    print('mean angle deg', angleNormLim )
                    tourner(angleNormLim, 1)
                    avancer(0.35,1)
    
        img2 = concatene(new_list)
        cv2.imshow('image',img2)
        cv2.waitKey(0)

#q.stop()
cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
