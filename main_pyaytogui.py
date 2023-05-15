import numpy as np
import cv2
import HandTrackingModule as htm
import time
import pyautogui 
 
##########################
wCam, hCam = 640, 480
# frameR = 150 # Frame Reduction
y_ = [50,200]
x_ = [100,100]

smoothening = 7
#########################
 
(wScr,hScr) = pyautogui.size()

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
    img = cv2.blur(img, (5,5))
    if(not success):
        continue
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
    
    fingers = detector.fingersUp()
    cv2.rectangle(img, (x_[0], y_[0]), (wCam - x_[1], hCam - y_[1]),
    (255, 0, 255), 2)
    if fingers[0]:
        pass
    elif fingers[4]:
        if fingers[1]:
            pyautogui.scroll(1)
        elif fingers[2]:
            pyautogui.scroll(-1)
    else:
        if fingers[1] == 1:
            x3 = np.interp(x1, (x_[0], wCam - x_[1]), (0, wScr))
            y3 = np.interp(y1, (y_[0], hCam - y_[1]), (0, hScr))
            # 6. Smoothen Values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
            pyautogui.moveTo(wScr - clocX, clocY)
            plocX, plocY = clocX, clocY
            
        if fingers[2] == 1:
            if c:
                pyautogui.mouseDown(button='left')
            c = False
        elif not c:
            c = True
            pyautogui.mouseUp(button='left')

        if fingers[3] == 1:
            if d_c:
                pyautogui.mouseDown(button='right')
            d_c = False
        elif not d_c:
            d_c = True
            pyautogui.mouseUp(button='right')
    
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
    (255, 0, 0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)