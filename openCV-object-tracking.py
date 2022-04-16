
# Object Thresholding and Tracking with OpenCV
# HSV threshold has been set to track an orange

import numpy as np
import cv2

def disp_text(guidance, status):
    cv2.putText(frame, status, (100,55), cv2.FONT_HERSHEY_COMPLEX_SMALL, .7, (0, 0, 255), 1, cv2.LINE_AA)
    cv2.putText(frame, guidance, (120,80), cv2.FONT_HERSHEY_COMPLEX_SMALL, .7, (0, 0, 255), 1, cv2.LINE_AA)

# Initialize webcam 
cap = cv2.VideoCapture(0)

#HSV values for an orange
lower_orange = np.array([11, 120, 142]) 
upper_orange = np.array([22, 203, 255])

while(True):

    # Capture frame
    ret, frame = cap.read()

    # Convert frame to HSV and isolate orange color
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 
    mask = cv2.inRange(hsv, lower_orange, upper_orange)

    # Find centroid of orange area
    M = cv2.moments(mask)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        cv2.drawMarker(frame, (cX, cY), (0,0,255), cv2.MARKER_CROSS, 60, 2, 8)
    else:
        cX, cY = "", ""

    # ------ HUD ------

    # HUD Visuals
    cv2.drawMarker(frame, (320, 240), (255,255,255), cv2.MARKER_CROSS, 640, 1, 8)
    frame = cv2.copyMakeBorder(frame, 5, 5, 5, 5, borderType = cv2.BORDER_CONSTANT, value = [0,0,0])
    cv2.putText(frame, 'STATUS: ', (25,55), cv2.FONT_HERSHEY_COMPLEX_SMALL, .7, (0, 0, 255), 1, cv2.LINE_AA)
    cv2.putText(frame, 'GUIDANCE: ', (25,80), cv2.FONT_HERSHEY_COMPLEX_SMALL, .7, (0, 0, 255), 1, cv2.LINE_AA)

    # Guidance 
    if not cX and not cY:
        disp_text('DISPLAY OBJECT', 'NO OBJECT DETECTED')

    elif cX < 315 and cY < 235:
        disp_text('MOVE CAMERA RIGHT-UP','OBJECT DETECTED')

    elif cX > 325 and cY < 235:
        disp_text('MOVE CAMERA LEFT-UP','OBJECT DETECTED')

    elif cX < 315 and cY > 245:
        disp_text('MOVE CAMERA RIGHT-DOWN','OBJECT DETECTED')

    elif cX > 325 and cY > 245:
        disp_text('MOVE CAMERA LEFT-DOWN', 'OBJECT DETECTED')

    elif cX >= 315 and cX <= 325 and cY <= 245 and cY >= 235:
        disp_text('CENTERED','OBJECT DETECTED')

    elif cX >= 315 and cX <= 325 and cY > 245:
        disp_text('MOVE CAMERA DOWN','OBJECT DETECTED')

    elif cX >= 315 and cX <= 325 and cY < 235:
        disp_text('MOVE CAMERA UP','OBJECT DETECTED')

    elif cY <= 245 and cY >= 235 and cX > 325:
        disp_text('MOVE CAMERA LEFT','OBJECT DETECTED')

    elif cY <= 245 and cY >= 235 and cX < 325:
        disp_text('MOVE CAMERA RIGHT','OBJECT DETECTED')
    
    # Show frame
    cv2.imshow('regular', frame) #display each frame (frame name, frame)

    # 'q' to close program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break