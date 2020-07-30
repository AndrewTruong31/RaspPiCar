import numpy as np
import cv2


cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()

    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #converts frame to grayscale
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #converts frame to hsl 


    #Red colour
    sensitivity = 25 #this sensitivity requires good lighting but is more accurate
    low_white = np.array([0, 0, 255 - sensitivity])
    high_white = np.array([255, sensitivity, 255])

    mask = cv2.inRange(hsv_frame, low_white, high_white)

    
    # cv2.imshow('hsv frame', hsv_frame)

    crop_left = mask[0:480, 0:320]
    cv2.imshow('Left crop', crop_left)

    crop_right = mask[0:480, 320:640]
    cv2.imshow('Right crop', crop_right)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(frame, contours, -1, (0,255,0), 3) #draws the contour on the frame

    #draws rectangles over all detectected white areas
    # if (len(contours)) > 0:
    #     for cnt in contours:
    #     # white_area = max(contours, key=cv2.contourArea)
    #         x, y, w, h = cv2.boundingRect(cnt)
    #         cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 0, 255), 2)

    tot_left = crop_left.size
    tot_right = crop_right.size

    left_white = np.count_nonzero(crop_left)
    right_white = np.count_nonzero(crop_right)

    left_percent = round(left_white * 100 / tot_left, 2)
    right_percent = round(right_white * 100 / tot_right, 2)

    print('L: ' + str(left_percent) + '%     R: ' + str(right_percent) + '%')

    cv2.imshow('frame', frame) #Displays the frame

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
        

cap.release()
cv2.destroyAllWindows()