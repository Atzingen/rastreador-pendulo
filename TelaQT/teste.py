# -*- coding: latin-1 -*-
import cv2
import numpy as np
import time
import matplotlib.pyplot as plt

arquivo = 'livre.mov'

# Valores iniciais para os parâmetros a serem testados (detector de objetos redondos)
blur = 5        # variável de cv2.medianBlur - número de pontos ao redor po pixel a ser "turvado"
dp   = 1        #
mind = 200      # Distância mínima entre um objeto detectado e um outro possível objeto
pr1  = 25       #
pr2  = 25       #
rmin = 5        # Raio minimo para ser considerado um objeto circular (em pixels)
rmax = 20       # Raio máximo para ser considerado um objeto circular (em pixels)

cv2.namedWindow("preview", 1)
capture = cv2.VideoCapture(arquivo)

t0        = time.time()
ct = 1
pos_theta    = np.zeros(1000)
pos_theta[0] = 300
pos_theta[1] = 300
tempo        = np.zeros(1000)
tempo[0]     = 0
tempo[1]     = 0.001

for i in range(2,1000):
    tempo[i] = np.nan
    pos_theta[i] = np.nan

plt.ion()
fig = plt.figure()
axes = fig.add_subplot(111)
line, = plt.plot(tempo, pos_theta)

while True:
    _, frame = capture.read()
    if frame is not None:
        try:
            frame = cv2.flip(frame,1,frame)
            frame2 = cv2.blur(frame,(9,9))                      # blur na imagem para retirar erros
            hsv = cv2.cvtColor(frame2,cv2.COLOR_BGR2HSV)        # converte os valors da imagem de rgb para hsv
            thresh = cv2.inRange(hsv,np.array((0, 100, 100)), np.array((30, 255, 255)))   # procura valores na imagem no range especificado (min e max)
            thresh = cv2.blur(thresh,(9,9))                     # blur na imagem com a cor filtrada
            cir = cv2.HoughCircles(thresh,cv2.HOUGH_GRADIENT,dp,mind,param1=pr1,param2=pr2,minRadius=rmin,maxRadius=rmax)  # encontra os objetos  circulares
            if cir is not None:                                 # Se encontrou um círculo
                for i in cir:
                    for j in i:
                        if j[0] > 0:
                            cv2.circle(frame,(j[0],j[1]), j[2], (255,0,0),5)
                            print(f'x={j[0]} \t y={j[1]}')
                            ct += 1
                            tempo[ct]     = time.time() - t0
                            pos_theta[ct] = j[0]
                            line.set_ydata(pos_theta)
                            line.set_xdata(tempo)
                            axes.relim()
                            axes.autoscale_view(True,True,True)
                            plt.draw()
            cv2.imshow("preview", frame)
        except:
            pass

    if cv2.waitKey(1) & 0xFF == ord('q'):       # fecha o programa quando a tecla q é pressionada
        capture.release()
        cv2.destroyAllWindows()
        break

plt.close()