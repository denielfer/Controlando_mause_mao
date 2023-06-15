import numpy as np
import cv2
import HandTrackingModule as htm
import time
import mouse 
from screeninfo import get_monitors

##########################
wCam, hCam = 640, 480
# frameR = 150 # Frame Reduction
y_ = [50,200]
x_ = [100,100]

smoothening = 7
#########################
 
# cv2.namedWindow("dst", cv2.WND_PROP_FULLSCREEN)
# cv2.setWindowProperty("dst",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
# (a,b,wScr,hScr) = cv2.getWindowImageRect('dst')
# cv2.destroyAllWindows()

wScr = get_monitors()[0].width
hScr = get_monitors()[0].height

###
c = True
d_c = True
pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0
 


cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1)



while True:
    success, img = cap.read()
    # cv2.normalize(img,img)
    if(not success):
        continue
    img = cv2.blur(img, (5,5))
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
    if len(lmList) != 0:
        x1, y1 = lmList[5][1:]
    
    fingers = detector.fingersUp()
    print(fingers)
    cv2.rectangle(img, (x_[0], y_[0]), (wCam - x_[1], hCam - y_[1]),
    (255, 0, 255), 2)
    if fingers[4] == 0 and fingers[0] == 1:
        if fingers[1] == 0:
            mouse.wheel(1)
        elif fingers[2] == 0:
            mouse.wheel(-1)
    elif fingers[1] == fingers[2] and fingers[1]== 1:
        x3 = np.interp(x1, (x_[0], wCam - x_[1]), (0, wScr))
        y3 = np.interp(y1, (y_[0], hCam - y_[1]), (0, hScr))
        # 6. Smoothen Values
        clocX = plocX + (x3 - plocX) / smoothening
        clocY = plocY + (y3 - plocY) / smoothening
        mouse.move(wScr - clocX, clocY)
        plocX, plocY = clocX, clocY
    else:
        if fingers[1] == 0:
            if c:
                mouse.press('left')
            c = False
        elif not c:
            c = True
            mouse.release('left')

        if fingers[2] == 0:
            if d_c:
                mouse.press('right')
            d_c = False
        elif not d_c:
            d_c = True
            mouse.release('right')
        
    
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
    (255, 0, 0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)