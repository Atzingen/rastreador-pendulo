import cv2
import numpy as np
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

arquivo = config['default']['video']

pontos = []
#arquivo = '../videos/VID-20200918-WA0013.mp4'
posicao = 1
new = False

def frame_change(pos):
    global posicao, new
    posicao = pos
    new = True

def click_event(event, x, y, flags, param):
    global pontos
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(pontos) < 1:
            pontos = [(x, y)]
        elif len(pontos) > 2:
            pontos = []
        else:
            pontos.append((x, y))
            cv2.line(image, pontos[0], pontos[1], (0, 255, 255), 2)
            pixel_distance = np.sqrt((pontos[0][0]-pontos[1][0])**2+(pontos[0][1]-pontos[1][1])**2)
            cv2.putText(image, f'{pixel_distance:.2f} Pixels', 
                        (int((pontos[0][0]+pontos[1][0])/2)+20, int((pontos[0][1]+ pontos[1][1])/2)), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.circle(image, (x, y), 10, (0, 0, 255), 2)
        cv2.imshow("image", image)

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