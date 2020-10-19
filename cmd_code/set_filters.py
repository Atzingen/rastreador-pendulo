import cv2
import numpy as np
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

arquivo = config['default']['video']

pontos = []
posicao = 1
new = False

def frame_change(pos):
    global posicao, new
    posicao = pos
    new = True

capture = cv2.VideoCapture(arquivo)
_, image = capture.read()

image_line1 = np.hstack((image, image))
image_line2 = np.hstack((image, image))
image = np.vstack((image_line1, image_line2))

cv2.namedWindow("image")
cv2.createTrackbar('Frame','image',0,int(capture.get(cv2.CAP_PROP_FRAME_COUNT)),frame_change)

blur = 9
Bsize = 15
rmin =  Bsize - int(Bsize/3)       # Raio minimo para ser considerado um objeto circular (em pixels)
rmax =  Bsize + int(Bsize/3)  
Hmin =  0 
Hmax =  50
Smin =  0
Smax =  100
Vmin =  0
Vmax =  100

while True:
    if new:
        new = False
        capture.set(cv2.CAP_PROP_POS_FRAMES, posicao)
        _, image_raw = capture.read()
        image_blur = cv2.blur(image_raw, (blur, blur))
        image_line1 = np.hstack((image_raw, image_blur))

        image_hsv = cv2.cvtColor(image_blur, cv2.COLOR_BGR2HSV)
        image_thresh = cv2.inRange(image_hsv,np.array((0, 100, 100)), np.array((30, 255, 255))) 
        image_thresh = cv2.blur(image_thresh,(blur, blur))
        image_thresh = cv2.cvtColor(image_thresh, cv2.COLOR_GRAY2BGR)
        cir = cv2.HoughCircles(image_thresh,cv2.HOUGH_GRADIENT,1,200,
                               param1=25,param2=25,minRadius=rmin,maxRadius=rmax) 
            if cir is not None:                                 # Se encontrou um círculo
                for i in cir:
                    for j in i:
                        if j[0] > 0:
                            cv2.circle(frame,(j[0],j[1]), int(j[2]), (255,255,0),5)
                            print(f'x={j[0]} \t y={j[1]}')


        image_line2 = np.hstack((image_thresh, image_blur))
        image = np.vstack((image_line1, image_line2))

    cv2.imshow("image", image)
    key = cv2.waitKey(1) & 0xFF

    # r para resset
    if key == ord("r"):
        capture.set(cv2.CAP_PROP_POS_FRAMES, posicao)
        _, image = capture.read()
        pontos = []
    elif key == ord("q"):
        break

print(f'P1 = {pontos[0][0]},{pontos[0][1]}  P2 = {pontos[1][0]},{pontos[1][1]}')
print(f'Pixel distance: {np.sqrt((pontos[0][0]-pontos[1][0])**2+(pontos[0][1]-pontos[1][1])**2)}')

cv2.destroyAllWindows()

# salvar valor no config