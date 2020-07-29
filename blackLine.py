import numpy as np
import cv2


def main():
    cap = cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)
    cap.set(5,30)

    while(True):
        ret, frame = cap.read()

        crop_frame = []
        cnt = []
        for i in range (4):
            crop_frame.append(frame[(i*120):((i+1)*120), 0:640])
            cnt.append(findContour(crop_frame[i]))
            if(len(cnt[i]) > 0):
                c = max(cnt[i], key=cv2.contourArea) #finds the contour with the largest area
                cv2.drawContours(crop_frame[i], cnt[i], -1, (0,255,0), 4) #draws the largest contour on the frame
                drawCenter(c, crop_frame[i])

        cv2.line(frame, (320, 0), (320, 480), (0, 0, 255),2) #draws a red line down the center of the frame 

    
        cv2.imshow('frame', frame)

        if cv2.waitKey(20) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def findContour(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #converts the coloured frame into grayscale
    blur_frame = cv2.GaussianBlur(gray_frame,(5,5),0) 
    ret, thresh = cv2.threshold(blur_frame, 40, 255, cv2.THRESH_BINARY_INV) #removes all non-black objects from frame
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #finds all of the contours on the frame
    return contours

def drawCenter(c, frame):

    x, y, w, h = cv2.boundingRect(c) #returns the coresponding values creating a rect around the contour
    M = cv2.moments(c)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    cv2.circle(frame, (cx,cy), 5, (255,0,0), 2)
    cv2.putText(frame, str(abs(320-cx)), (cx,cy+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)




if __name__ == '__main__':
    main()