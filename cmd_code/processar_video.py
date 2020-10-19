# -*- coding: latin-1 -*-
import cv2
import numpy as np
import time
import matplotlib.pyplot as plt
import configparser
import pickle

config = configparser.ConfigParser()
config.read('config.ini')

arquivo = config['default']['video']
blur = int(config['default']['blur'])        # variável de cv2.medianBlur - número de pontos ao redor po pixel a ser "turvado"
Hmin = int(config['default']['Hmin'])        # Filtros para o HSV
Hmax = int(config['default']['Hmax'])
Smin = int(config['default']['Smin'])
Smax = int(config['default']['Smax'])
Vmin = int(config['default']['Vmin'])
Vmax = int(config['default']['Vmax'])
dp   = 1        #
mind = 200      # Distância mínima entre um objeto detectado e um outro possível objeto
pr1  = 25       #
pr2  = 25       #
Bsize = int(config['default']['Bsize'])
rmin =  Bsize - int(Bsize/3)       # Raio minimo para ser considerado um objeto circular (em pixels)
rmax =  Bsize + int(Bsize/3)       # Raio máximo para ser considerado um objeto circular (em pixels)

cv2.namedWindow("preview", 1)
capture = cv2.VideoCapture(arquivo)
tam_vetor = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))

frame_count  = 0
fps          = 30
dt           = 1/fps
L            = float(config['default']['L'])    # comprimento em metros do fio
L_pixel      = float(config['default']['L_pixel'])   # comprimento em pixels do fio (obtido via get_size.py)
tam_vetor    = 100000
pos_x    = np.zeros(tam_vetor)
pos_x[0] = 0
tempo        = np.zeros(tam_vetor)
tempo[0]     = 0

for i in range(1, tam_vetor):
    tempo[i] = np.nan
    pos_x[i] = np.nan

plt.ion()
fig = plt.figure()
axes = fig.add_subplot(111)
line, = plt.plot(tempo, pos_x)
skip_count = 0

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
                            cv2.circle(frame,(j[0],j[1]), int(j[2]), (255,255,0),5)
                            print(f'x={j[0]} \t y={j[1]}')
                            frame_count += 1
                            tempo[frame_count]     = tempo[frame_count - 1] + dt
                            pos_x[frame_count] = j[0]*L/L_pixel
                            line.set_ydata(pos_x)
                            line.set_xdata(tempo)
                            axes.relim()
                            axes.autoscale_view(True,True,True)
                            plt.draw()
            else:
                skip_count += 1
                print(f"frame {frame_count} skip - n = {skip_count}")
            cv2.imshow("preview", frame)
        except Exception as e:
            print(f'except: {e}')
            pass
    else:
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):       # fecha o programa quando a tecla q é pressionada
        capture.release()
        cv2.destroyAllWindows()
        break



out = np.transpose(np.vstack((tempo, pos_x)))
out = out[~np.isnan(out[:,0])]

np.savetxt('resultado.csv', out, delimiter=',')

#input("programa terminado ... pressione qualquer tecla para sair")  # descomentar para evita de fechar o gráfico
plt.close()