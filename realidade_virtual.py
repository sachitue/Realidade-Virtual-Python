import cv2 
import numpy as np


#inicializamos los parametros del detector 
parametros = cv2.aruco.DetectorParameters_create()

#Cargamos el diccionario de nuestro aruco
diccionario=cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_100)

# Lectura de la camera

cap=cv2.VideoCapture(0)
cap.set(3,1280) #Definiremos un acho y un alto
cap.set(4,720)

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #Detectamos los marcadores en la imagem
    esquinas, ids, candidatos_malos=cv2.aruco.detectMarkers(gray, diccionario, parameters=parametros)
    
    if np.all(ids != None):
        aruco = cv2.aruco.drawDetectedMarkers(frame, esquinas)


        #Estraemos los puntos de la esquinas en coordenadas separadas
        c1=(esquinas[0][0][0][0], esquinas[0][0][0][1])
        c2=(esquinas[0][0][1][0], esquinas[0][0][1][1])
        c3=(esquinas[0][0][2][0], esquinas[0][0][2][1])
        c4=(esquinas[0][0][3][0], esquinas[0][0][3][1])

        copy = frame

        #Leemos la imagen que vamos a sobreponer
        imagen=cv2.imread("images.JPG")
        #Extraemos las coordenadas del aruco en una matriz
        tamanho=imagen.shape
        #Organizamos las coordenadas del aruco en una matriz
        puntos_aruco=np.array([c1,c2,c3,c4])

        #Organizamos las cooredenadas de la imagen otra matriz
        puntos_imagen=np.array([
            [0,0],
            [tamanho[1]-1,0],
            [tamanho[1]-1, tamanho[0]-1],
            [0, tamanho[0]-1]
            ], dtype=float)

         
         #Realizamos la superposicion de la imagen (Homografia)
        h, estado= cv2.findHomography(puntos_imagen, puntos_aruco)

         #Realizamos la transformacion de perspectiva
        perspectiva= cv2.warpPerspective(imagen, h,(copy.shape[1], copy.shape[0]))
        cv2.fillConvexPoly(copy, puntos_aruco.astype(int),0,16)
        copy=copy + perspectiva
        cv2.imshow("Realidad Virtual", copy)
    
    else:
        cv2.imshow('Realiad Virtual', frame)

    k=cv2.waitKey(1)
    if k==27:
        break   
cap.release()
cv2.destroyWindow()




