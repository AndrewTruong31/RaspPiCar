import numpy as np
import cv2


def main():
    cap = cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)
    cap.set(5,30)

    while(True):
        ret, frame = cap.read()

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #converts the coloured frame into grayscale
        ret, thresh = cv2.threshold(gray_frame, 40, 255, cv2.THRESH_BINARY_INV) #removes all non-black objects from frame
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #finds all of the contours on the frame
        cv2.line(frame, (320, 0), (320, 480), (0, 0, 255),2) #draws a red line down the center of the frame

        

        drawCircle(contours, frame)

        #iterates through all the contours on the frame
        # if (len(contours)) > 0:
        #     for cnt in contours:
        #     # white_area = max(contours, key=cv2.contourArea)
        #         x, y, w, h = cv2.boundingRect(cnt)
        #         cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 0, 255), 2)

        cv2.imshow('black', thresh)
        cv2.imshow('frame', frame)

        if cv2.waitKey(20) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()



def drawCircle(contours, frame):
    if(len(contours) > 0):
        c = max(contours, key=cv2.contourArea) #finds the contour with the largest area
        cv2.drawContours(frame, c, -1, (0,255,0), 3) #draws the largest contour on the frame

        x, y, w, h = cv2.boundingRect(c) #returns the coresponding values creating a rect around the contour
        cx = int(x + (w/2))
        cy = int(y + (h/2))
        cv2.circle(frame, (cx,cy), 3, (255, 255, 255), 2)




if __name__ == '__main__':
    main()