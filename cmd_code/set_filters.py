import cv2
import numpy as np
import configparser
from configparser import SafeConfigParser

def frame_change(pos):
    global posicao, new
    posicao = pos
    new = True

def sliders_update(val):
    global new
    new = True

def main():
    config = configparser.ConfigParser()
    config.read('config.ini')

    arquivo = config['default']['video']

    font = cv2.FONT_HERSHEY_SIMPLEX

    posicao = 1
    new = False

    capture = cv2.VideoCapture(arquivo)
    _, image = capture.read()

    image_line1 = np.hstack((image, image))
    image_line2 = np.hstack((image, image))
    image = np.vstack((image_line1, image_line2))

    blur = int(config['default']['blur'])
    Bsize = int(config['default']['Bsize'])
    Hmin = int(config['default']['Hmin'])
    Hmax = int(config['default']['Hmax'])
    Smin = int(config['default']['Smin'])
    Smax = int(config['default']['Smax'])
    Vmin = int(config['default']['Vmin'])
    Vmax = int(config['default']['Vmax'])

    cv2.namedWindow("image")
    cv2.createTrackbar('Frame','image',0,int(capture.get(cv2.CAP_PROP_FRAME_COUNT)),frame_change)
    cv2.createTrackbar('Blur','image',blur,30,sliders_update)
    cv2.createTrackbar('Hmin','image',Hmin,100,sliders_update)
    cv2.createTrackbar('Hmax','image',Hmax,179,sliders_update)
    cv2.createTrackbar('Smin','image',Smin,255,sliders_update)
    cv2.createTrackbar('Smax','image',Smax,255,sliders_update)
    cv2.createTrackbar('Vmin','image',Vmin,255,sliders_update)
    cv2.createTrackbar('Vmax','image',Vmax,255,sliders_update)
    cv2.createTrackbar('Bsize','image',Bsize,50,sliders_update)



    rmin =  Bsize - int(Bsize/3)       # Raio minimo para ser considerado um objeto circular (em pixels)
    rmax =  Bsize + int(Bsize/3)  

    while True:
        if new:
            new = False
            capture.set(cv2.CAP_PROP_POS_FRAMES, posicao)
            _, image_raw = capture.read()
            blur = int(cv2.getTrackbarPos('Blur', 'image'))
            if blur%2 == 0: 
                blur += 1
            Hmin = int(cv2.getTrackbarPos('Hmin', 'image'))
            Hmax = int(cv2.getTrackbarPos('Hmax', 'image'))
            Smin = int(cv2.getTrackbarPos('Smin', 'image'))
            Smax = int(cv2.getTrackbarPos('Smax', 'image'))
            Vmin = int(cv2.getTrackbarPos('Vmin', 'image'))
            Vmax = int(cv2.getTrackbarPos('Vmax', 'image'))
            Bsize = int(cv2.getTrackbarPos('Bsize', 'image'))
            Hmax = int(cv2.getTrackbarPos('Hmax', 'image'))
            # TODO: max nao pode ser menor que min para H, S e V

            image_blur = cv2.blur(image_raw, (blur, blur))

            image_hsv = cv2.cvtColor(image_blur, cv2.COLOR_BGR2HSV)
            image_thresh = cv2.inRange(image_hsv,np.array((Hmin, Smin, Vmin)), np.array((Hmax, Smax, Vmax))) 
            image_thresh = cv2.blur(image_thresh,(blur, blur))
            try:
                rmin =  Bsize - int(Bsize/3) 
                rmax =  Bsize + int(Bsize/3)
                print(rmin, rmax)
                cir = cv2.HoughCircles(image_thresh,cv2.HOUGH_GRADIENT,1,200,
                                param1=25,param2=25,minRadius=5,maxRadius=20) 
                if cir is not None:
                    for i in cir:
                        for j in i:
                            if j[0] > 0:
                                cv2.circle(image_raw,(j[0],j[1]), int(j[2]), (255,255,0),5)
                                print(f'x={j[0]} \t y={j[1]}')
            except Exception as e:
                print('Exception: ', e)


            cv2.putText(image_raw,'sair:   q',(10,30), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.putText(image_raw,'reset:  r',(10,90), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.putText(image_raw,'Salvar: s',(10,150), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
            image_line1 = np.hstack((image_raw, image_blur))
            image_thresh = cv2.cvtColor(image_thresh, cv2.COLOR_GRAY2BGR)
            image_line2 = np.hstack((image_thresh, image_blur))
            image = np.vstack((image_line1, image_line2))

        cv2.imshow("image", image)
        key = cv2.waitKey(1) & 0xFF

        # r para resset
        if key == ord("r"):
            posicao = 1
            capture.set(cv2.CAP_PROP_POS_FRAMES, posicao)
            _, image = capture.read()
        elif key == ord('s'):
            blur = int(cv2.getTrackbarPos('Blur', 'image'))
            if blur%2 == 0: 
                blur += 1
            Hmin = int(cv2.getTrackbarPos('Hmin', 'image'))
            Hmax = int(cv2.getTrackbarPos('Hmax', 'image'))
            Smin = int(cv2.getTrackbarPos('Smin', 'image'))
            Smax = int(cv2.getTrackbarPos('Smax', 'image'))
            Vmin = int(cv2.getTrackbarPos('Vmin', 'image'))
            Vmax = int(cv2.getTrackbarPos('Vmax', 'image'))
            Bsize = int(cv2.getTrackbarPos('Bsize', 'image'))

            parser = SafeConfigParser()
            parser.read('config.ini')
            parser.set('atual', 'blur', str(blur))
            parser.set('atual', 'Hmin', str(Hmin))
            parser.set('atual', 'Smin', str(Smin))
            parser.set('atual', 'Smax', str(Smax))
            parser.set('atual', 'Vmin', str(Vmin))
            parser.set('atual', 'Vmax', str(Vmax))
            parser.set('atual', 'Bsize', str(Bsize))

            with open('config.ini', 'w+') as configfile:
                parser.write(configfile)

        elif key == ord("q"):
            break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()