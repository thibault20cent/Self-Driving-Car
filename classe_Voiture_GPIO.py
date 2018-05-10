import RPi.GPIO as GPIO
from math import *
import time

#Parametres moteur
FREQ_COMMANDE_MOTEUR=50
     
#Vitesse en m/s
VITESSE_1=0.3
VITESSE_2=0.4
VITESSE_3=0.5

# Ports
PORT_MOTEUR_VITESSE=18
PORT_MOTEUR_DIRECTION=19

#Declaration des ports
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(PORT_MOTEUR_VITESSE, GPIO.OUT)
GPIO.setup(PORT_MOTEUR_DIRECTION, GPIO.OUT)  
p=GPIO.PWM(PORT_MOTEUR_VITESSE, FREQ_COMMANDE_MOTEUR)
q=GPIO.PWM(PORT_MOTEUR_DIRECTION, FREQ_COMMANDE_MOTEUR)

def avancer_tourner(vitesse, angle, duree):
    tourner(angle,0.2)
    avancer(vitesse, duree)

def av_rap_cyc():
    rap_cyc=1
    while (rap_cyc<50):
        p.start(rap_cyc)
        time.sleep(2) #duree entre deux impulsions
        rap_cyc=rap_cyc+5
    p.stop()

def avancer(vitesse,duree):
    #tab_impulsion = [1.5,1.4,1.3,1.2,1]    #duree des impulsions en ms
    tab_impulsion = [1.3,1.25,1.2]
    n=0
    if (vitesse<0):
        reculer(-vitesse,duree) #si la vitesse entree est negative, on recule
    else :
        if (0<=vitesse < VITESSE_1):
            print("ca n avance pas")
            arreter()
            
        elif (VITESSE_1<=vitesse<VITESSE_2):
            n=0
        elif (VITESSE_2<=vitesse<VITESSE_3):
            n=1
        else :
            n=2
    
        rap_cyc = tab_impulsion[n]*0.001*FREQ_COMMANDE_MOTEUR#'entier inf
        
        print("impulsion = ",tab_impulsion[n],"\n")
        print("rapport cyclique = ",rap_cyc)
        
        p.ChangeDutyCycle(rap_cyc*100)
        time.sleep(duree) #duree de l impulsion 
        

def reculer(vitesse,duree):
    tab_impulsion_recul = [1.54,1.58,1.62] #duree des impulsions en ms
    n=0
    if (vitesse<0):
        vitesse = -vitesse  #si la vitesse en entree est negative, on recule quand meme
    else :
        if (0<=vitesse < VITESSE_1):
            print("ca n avance pas")
            arreter()
            
        elif (VITESSE_1<=vitesse<VITESSE_2):
            n=0
        elif (VITESSE_2<=vitesse<VITESSE_3):
            n=1
        else :
            n=2
    rap_cyc = tab_impulsion_recul[n]*0.001*FREQ_COMMANDE_MOTEUR
    print("impulsion = ",tab_impulsion_recul[n],"\n")
    print("rapport cyclique = ",rap_cyc)
    p.ChangeDutyCycle(rap_cyc*100 )
    time.sleep(duree) #duree entre deux impulsions


def arreter(duree):
    print("stop")
    p.ChangeDutyCycle(0)
    time.sleep(duree)
	
def tourner_imp (duree_imp,duree):
    rap_cyc = duree_imp*0.001*FREQ_COMMANDE_MOTEUR
    print("duree impulsion =", duree_imp)
    print("rapport cyclique = ",rap_cyc)
    q.start(rap_cyc*100)
    time.sleep(duree)
    q.stop

def tourner (angle,duree):
    q=GPIO.PWM(PORT_MOTEUR_DIRECTION, FREQ_COMMANDE_MOTEUR)
    #angle<0 : gauche ; angle>0 : droite
    angle_max_droite=25.0
    angle_max_gauche=-25.0
    impulsion_max_droite=1.8
    impulsion_max_gauche=0.8
    impulsion_angle_nul=1.45
    duree_impulsion=0.0
    if angle>angle_max_droite :
        angle = angle_max_droite
        print("coucou 1")
    elif angle<angle_max_gauche :
        angle = angle_max_gauche
        print("coucou 2")
    if angle<0 :#tourner a gauche
       duree_impulsion=impulsion_angle_nul-(angle/angle_max_gauche)*(impulsion_angle_nul-impulsion_max_gauche)
       print("coucou 3")
    elif angle>0: # tourner a droite
        duree_impulsion=impulsion_angle_nul+(angle/angle_max_droite)*(impulsion_max_droite-impulsion_angle_nul)
        print("coucou 4")
        print("duree impulsion : ", duree_impulsion)
        print("angle : ", angle)
        print("angle_max_droite : ", angle_max_droite)
        print("imp_nulle : ", impulsion_angle_nul)
    else:
        duree_impulsion=impulsion_angle_nul
        print("coucou 5")
    rap_cyc = duree_impulsion*0.001*FREQ_COMMANDE_MOTEUR
   #rap_cyc = floor(RANGE*duree_impulsion*FREQ_COMMANDE_MOTEUR)
    print("duree impusion =", duree_impulsion)
    print("rapport cyclique = ",rap_cyc)
    q.start(rap_cyc*100)
    time.sleep(duree)
    q.stop

        
# pour ne pas se prendre la tete avec des histoires de signe, on pourra utiliser ces fonctions plutot que "tourner"
def tourner_gauche(angle, duree):
    if angle>=0 :
        tourner(-angle, duree)
    else :
        tourner(angle, duree)

def tourner_droite(angle, duree):
    if angle>=0:
        tourner(angle, duree)
    else :
        tourner(-angle, duree)

#si on a un moyen de mesurer la vitesse 
def corriger_vitesse():
    print("on corrige\n")
    
    

