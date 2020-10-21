import cv2
import numpy as np
import configparser

pontos = []
new = False
x, y = 0, 0

def frame_change(pos):
    print('frame change')
    global posicao, new
    posicao = pos
    new = True

def click_event(event, x_i, y_i, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print('click_event')
        global pontos, new, x, y
        x, y = x_i, y_i
        if len(pontos) < 1:
            pontos = [(x, y)]
        elif len(pontos) > 2:
            pontos = []
        else:
            pontos.append((x, y))
        new = True

def main():
    global new, pontos, x, y
    config = configparser.ConfigParser()
    config.read('config.ini')

    arquivo = config['default']['video']

    font = cv2.FONT_HERSHEY_SIMPLEX

    #arquivo = '../videos/VID-20200918-WA0013.mp4'
    posicao = 1
    new = False

    capture = cv2.VideoCapture(arquivo)
    _, image = capture.read()

    cv2.namedWindow("image")
    cv2.setMouseCallback("image", click_event)
    cv2.createTrackbar('Frame','image',0,int(capture.get(cv2.CAP_PROP_FRAME_COUNT)),frame_change)

    while True:
        if new:
            new = False
            capture.set(cv2.CAP_PROP_POS_FRAMES, posicao)
            print(posicao)
            _, image = capture.read()
            if len(pontos) == 2:
                cv2.line(image, pontos[0], pontos[1], (0, 255, 255), 2)
                pixel_distance = np.sqrt((pontos[0][0]-pontos[1][0])**2+(pontos[0][1]-pontos[1][1])**2)
                cv2.putText(image, f'{pixel_distance:.2f} Pixels', 
                            (int((pontos[0][0]+pontos[1][0])/2)+20, int((pontos[0][1]+ pontos[1][1])/2)), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.circle(image, (x, y), 10, (0, 0, 255), 2)
            cv2.putText(image,'sair:   q',(10,30), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.putText(image,'reset:  r',(10,90), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.putText(image,'Salvar: s',(10,150), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.imshow("image", image)

        key = cv2.waitKey(1) & 0xFF

        # r para resset
        if key == ord("r"):
            capture.set(cv2.CAP_PROP_POS_FRAMES, posicao)
            _, image = capture.read()
            pontos = []
            new = True
        elif key == ord("q"):
            break
        elif key == ord("s"):
            pass # TODO - Salvar no config

    print(f'P1 = {pontos[0][0]},{pontos[0][1]}  P2 = {pontos[1][0]},{pontos[1][1]}')
    print(f'Pixel distance: {np.sqrt((pontos[0][0]-pontos[1][0])**2+(pontos[0][1]-pontos[1][1])**2)}')

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()